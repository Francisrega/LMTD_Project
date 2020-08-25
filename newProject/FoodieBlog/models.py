from django.db import models


# Create your models here.

class Student(models.Model):
    firstname = models.CharField(max_length=32)
    email = models.EmailField()

    def __str__(self):
        return self.firstname