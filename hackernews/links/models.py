from django.db import models


class Link(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True)


class User(models.Model):
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    email = models.EmailField()
