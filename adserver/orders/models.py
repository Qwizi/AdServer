import uuid

from django.conf import settings
from django.db import models


class Order(models.Model):

    class OrderStatus(models.TextChoices):
        CREATED = "created", "Utworzono"
        PAID = "paid", "Zapłacono"
        FAILED = "failed", "Wystapil blad"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    name = models.CharField(max_length=64, default="Doładowanie portfela")
    status = models.CharField(max_length=7, choices=OrderStatus.choices, default=OrderStatus.CREATED)
    amount = models.IntegerField(default=200)
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    stripe_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.name} | {self.amount} | {self.user.username}"
