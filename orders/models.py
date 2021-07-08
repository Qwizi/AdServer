import decimal
import uuid

from django.conf import settings
from django.db import models


class OrderStatus(models.TextChoices):
    CREATED = "created", "Utworzono"
    PAID = "paid", "Zapłacono"
    FAILED = "failed", "Wystapil blad"


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    name = models.CharField(max_length=64, default="Doładowanie portfela")
    status = models.CharField(max_length=7, choices=OrderStatus.choices, default=OrderStatus.CREATED)
    amount = models.IntegerField(default=200)
    created_at = models.DateTimeField(auto_now=True, auto_created=True)
    stripe_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} | {self.amount} | {self.user.username}"

    def get_formatted_amount(self):
        return decimal.Decimal('{:,.2f}'.format(self.amount / 100))
