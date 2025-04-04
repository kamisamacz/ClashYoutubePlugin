from django.db import models

class User(models.Model):
    nickname = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.nickname


