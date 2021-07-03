import uuid

from django.conf import settings
from django.db import models


class Ad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ads")
    url = models.URLField()
    name = models.CharField(max_length=64)
    banner = models.ImageField(upload_to='uploads/', null=True)
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} | {self.name} | {self.user.username}"

    def charge(self, value):
        self.balance += value
