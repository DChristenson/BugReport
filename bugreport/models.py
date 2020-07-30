from django.db import models
from django.utils import timezone
from model_utils.fields import StatusField
from model_utils import Choices
from django.contrib.auth.models import User


class Ticket(models.Model):
    N = "New"
    IP = "In-Progress"
    D = "Done"
    INV = "Invalid"
    STATUS_CHOICES = [
        (N, "New"),
        (IP, "In-Progress"),
        (D, "Done"),
        (INV, "Invalid")
    ]
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=N)
    title = models.CharField(max_length=50)
    time = models.DateTimeField(default=timezone.now)
    body = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True,
                                      related_name="assigned_user")
    completed_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True,
                                     related_name="completed_by")

    def __str__(self):
        return f'{self.time} - {self.creator}'
