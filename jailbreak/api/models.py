# csv_app/models.py

from django.db import models


class Question(models.Model):
    goal = models.CharField(max_length=255)
    target = models.CharField(max_length=255)
    behavior = models.CharField(max_length=255)
    category = models.CharField(max_length=255)


class Set(models.Model):
    name = models.CharField(max_length=50, unique=True)
    relation = models.ManyToManyField(Question)



