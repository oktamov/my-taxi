from django.contrib import admin

from users.models import  User, VerificationCode


admin.site.register(User)
admin.site.register(VerificationCode)
