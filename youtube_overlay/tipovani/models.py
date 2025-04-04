from django.db import models
from django.contrib.auth.models import User
from poradatel.models import Kolo

class Tip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kolo = models.ForeignKey(Kolo, on_delete=models.CASCADE, related_name="tipy")
    vybrany_team = models.CharField(max_length=1, choices=[('A', 'Tým A'), ('B', 'Tým B')])

    class Meta:
        unique_together = ('user', 'kolo')

    def __str__(self):
        return f"{self.user.username} tipuje {self.vybrany_team} v kole {self.kolo.id}"
