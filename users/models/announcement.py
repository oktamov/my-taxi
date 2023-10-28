import datetime

from django.db import models

from common.models import Region
from users.models import User


class Announcement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcement')
    from_region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='user_from')
    to_region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='user_to')
    price = models.IntegerField(null=True, blank=True)
    seats = models.IntegerField(default=1)
    when = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.user.full_name

