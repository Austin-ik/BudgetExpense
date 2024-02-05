from django.db import models
from expTracker.permissions import IsOwner
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Expense(models.Model):

    CATEGORY = (
        ('ESSENTIALS', 'Essentials'),
        ('LUXURY', 'Luxury'),
        ('HEALTHCARE', 'Healthcare'),
        ('MISC', 'Misc')
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.IntegerField(default=0)
    category = models.CharField(max_length=50, choices=CATEGORY)
    description = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)

    class Meta:

        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.user.username}'s {self.category} expense"


class Budget(models.Model):

    CATEGORY = (
        ('ESSENTIALS', 'Essentials'),
        ('LUXURY', 'Luxury'),
        ('HEALTHCARE', 'Healthcare'),
        ('MISC', 'Misc')
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="budgets")
    category = models.CharField(max_length=50, choices=CATEGORY)
    amount = amount = models.IntegerField(default=0)

    class Meta:

        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.user.username}'s {self.category} budget"
