from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken

from users.manager import UserManager
from utils.regex import phone_regex


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=15,
        unique=True,
        error_messages={
            "unique": _("A user with that phone number already exists."),
        },
    )
    country = models.ForeignKey(
        "common.Country",
        models.SET_DEFAULT,
        to_field="code",
        default=settings.DEFAULT_COUNTRY_CODE,
        db_column="country_code",
    )
    profile_picture = models.ImageField(upload_to="profile_pictures", null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    USERNAME_FIELD = "phone_number"

    objects = UserManager()

    def __str__(self):
        return self.phone_number

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name).strip()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"access": str(refresh.access_token), "refresh": str(refresh)}
