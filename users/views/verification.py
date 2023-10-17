from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import PhoneVerifySerializer, SendVerificationCodeSerializer
from utils.exceptions import IncorrectCodeException
from utils.verification import (
    check_verification_code,
    get_verification_type,
    send_verification_code,
)


class SendVerificationCodeView(APIView):
    @swagger_auto_schema(request_body=SendVerificationCodeSerializer)
    def post(self, request):
        serializer = SendVerificationCodeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data.get("phone_number")
            verification_type = get_verification_type(phone_number)
            send_verification_code(phone_number, verification_type)
            return Response({"detail": _("SMS sent successfully."), "verification_type": verification_type})


class PhoneVerifyView(APIView):
    @swagger_auto_schema(request_body=PhoneVerifySerializer)
    def post(self, request):
        serializer = PhoneVerifySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data.get("phone_number")
            code = serializer.validated_data.get("code")
            verification_type = get_verification_type(phone_number)
            if check_verification_code(phone_number, verification_type, code):
                if verification_type == 'login':
                    user = User.objects.get(phone_number=phone_number)
                    return Response({
                        'tokens': user.tokens(),
                        'user': {
                            'id': user.id,
                            'phone_number': user.phone_number,
                            # add other fields here if needed
                        }
                    })

                return Response({"detail": _("Phone is verified."), "verification_type": verification_type})
            else:
                raise IncorrectCodeException
