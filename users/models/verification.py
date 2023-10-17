from django.db import models
from django.utils import timezone

from common.models import BaseModel


class VerificationCode(BaseModel):
    class VerificationTypes(models.TextChoices):
        LOGIN = "login"
        REGISTER = "register"

    phone_number = models.CharField(max_length=15)
    code = models.CharField(max_length=100)
    signature = models.CharField(max_length=100, null=True, blank=True)
    verification_type = models.CharField(max_length=32, choices=VerificationTypes.choices)
    user = models.ForeignKey("users.User", models.CASCADE, "verification_codes", null=True, blank=True)
    attempts = models.PositiveSmallIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    expired_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["phone_number", "verification_type"]

    def __str__(self):
        return f"{self.phone_number} - {self.code}"

    @property
    def expired(self):
        return self.expired_at < timezone.now()
