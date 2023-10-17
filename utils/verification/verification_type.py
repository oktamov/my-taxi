from users.models import User, VerificationCode
from utils import get_or_none


def get_verification_type(phone_number):
    user = get_or_none(User, phone_number=phone_number)
    return VerificationCode.VerificationTypes.LOGIN if user else VerificationCode.VerificationTypes.REGISTER
