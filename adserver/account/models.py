from django.db import models
from django.conf import settings
from django.dispatch import receiver
from djoser.signals import user_registered


class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username} | {self.balance}"

    def recharge(self, value):
        self.balance += value

    def debit(self, value):
        self.balance -= value


@receiver(user_registered)
def create_wallet(user, request, **kwargs):
    wallet = Wallet.objects.create(user=user)
    print(f'User {user.username} zarejestrowal sie')
