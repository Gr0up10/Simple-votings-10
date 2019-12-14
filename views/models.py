from django.db import models

# Create your models here.


class Voting(models.Model):
    question = models.CharField(max_length=250)
    author = models.IntegerField()
    created = models.DateTimeField(auto_now=True)

    def options(self):
        return Option.objects.filter(voting=self)


class Option(models.Model):
    voting = models.ForeignKey(to=Voting,on_delete=models.CASCADE)
    text = models.CharField(max_length=50)