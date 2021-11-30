from django.contrib.auth.models import User
from django.db import models


class Desk(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=200)
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']
