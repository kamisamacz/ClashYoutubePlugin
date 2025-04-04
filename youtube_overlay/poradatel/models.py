from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    max_slots = models.IntegerField(default=0)
    participants = models.ManyToManyField(User, blank=True)

    @property
    def free_slots(self):
        return self.max_slots - self.participants.count()

    def __str__(self):
        return self.name


class Kolo(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="kola")
    zapasnik_a = models.CharField(max_length=100)
    zapasnik_b = models.CharField(max_length=100)
    uzavreno = models.BooleanField(default=False)
    vitez = models.CharField(
        max_length=1,
        choices=[("A", "Zápasník A"), ("B", "Zápasník B")],
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.zapasnik_a} vs {self.zapasnik_b} ({'Uzavřeno' if self.uzavreno else 'Otevřeno'})"
