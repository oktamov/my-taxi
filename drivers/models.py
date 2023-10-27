from django.db import models

from common.models import Region
from users.models import User


class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='drivers')
    from_region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='drivers_from')
    to_region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='drivers_to')
    price = models.IntegerField(null=True, blank=True)
    car = models.CharField(max_length=55)
    car_number = models.CharField(max_length=8)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.full_name} {self.from_region}-{self.to_region}"
