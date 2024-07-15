from django.db import models
import uuid
from django.core.validators import MinValueValidator
# Create your models here.
class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    balance = models.FloatField(default=0, validators=[MinValueValidator(0)], null=True, blank=True)

    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender_transactions', null=True, blank=True)
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver_transactions')
    amount = models.FloatField(default=0, validators=[MinValueValidator(0)])
    created_in = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_in']
    def __str__(self):
        return str(self.id)
