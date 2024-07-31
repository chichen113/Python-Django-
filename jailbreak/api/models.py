# csv_app/models.py
import datetime

from django.db import models


class Question(models.Model):
    goal = models.CharField(max_length=255)
    target = models.CharField(max_length=255)
    behavior = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=255)
    methods = models.CharField(max_length=50, default='无增强')


class Set(models.Model):
    name = models.CharField(max_length=50, unique=True)
    relation = models.ManyToManyField(Question)
    cate = models.CharField(max_length=50, default='jailbreak')


class Suite(models.Model):
    name = models.CharField(max_length=50, unique=True)
    time = models.DateTimeField(default=datetime.datetime.now)
    state = models.CharField(max_length=50)


class Test(models.Model):
    name = models.CharField(max_length=50, unique=True)
    collection = models.ForeignKey(Set, on_delete=models.CASCADE)
    model = models.CharField(max_length=50)
    evaluator = models.CharField(max_length=50)
    suite = models.ForeignKey(Suite, on_delete=models.CASCADE, null=True)


class Task(models.Model):
    name = models.CharField(max_length=50, unique=True)
    state = models.CharField(max_length=50, default='starting')
    escape_rate = models.CharField(max_length=50)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, null=True)
