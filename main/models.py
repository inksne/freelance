from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=256)
    customer = models.ForeignKey(User, verbose_name='пользователь', on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='orders/', null=True, blank=True)

    def __str__(self):
        return self.name