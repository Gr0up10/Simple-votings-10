from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Voting(models.Model):
    question = models.CharField(max_length=250)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=True)
    isCheckbox = models.BooleanField(default=False)  # переменная множественного выбора

    def options(self):
        return Option.objects.filter(voting=self)


class Option(models.Model):
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)

    def vote_count(self):
        return len(Vote.objects.filter(option=self))


class Vote(models.Model):
    option = models.ForeignKey(to=Option, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE, null=True, blank=True)

