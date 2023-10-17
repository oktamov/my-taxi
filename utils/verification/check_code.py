from users.models import VerificationCode
from utils.exceptions import ExpireVerificationCodeException


def check_verification_code(phone_number, verification_type, code):
    verification_code = VerificationCode.objects.filter(
        phone_number=phone_number, verification_type=verification_type, is_verified=False
    ).last()
    if verification_code:
        if verification_code.expired:
            raise ExpireVerificationCodeException
        if verification_code.code == code:
            verification_code.is_verified = True
            verification_code.save(update_fields=["is_verified"])
            return True
        return False
