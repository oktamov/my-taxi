from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class ExpireVerificationCodeException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Verification code is expired.")
    # default_code = 'parse_error'  # noqa E800


class IncorrectCodeException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Incorrect code.")
    # default_code = 'parse_error'  # noqa E800
