from django.contrib.auth.backends import ModelBackend, UserModel

from users.models import VerificationCode
from utils.exceptions import ExpireVerificationCodeException


class SMSSupportedAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = UserModel._default_manager.get_by_natural_key(username)  # noqa
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if self.user_can_authenticate(user):
                verification_code = user.verification_codes.filter(
                    verification_type=VerificationCode.VerificationTypes.LOGIN, is_verified=False
                ).last()
                if verification_code:
                    if verification_code.code == password and verification_code.attempts < 3:
                        if verification_code.expired:
                            raise ExpireVerificationCodeException
                        verification_code.is_verified = True
                        verification_code.save(update_fields=["is_verified"])
                        return user
                    else:
                        verification_code.attempts += 1
                        verification_code.save(update_fields=["attempts"])
                if user.check_password(password):
                    return user
