from django.db import models

# Create your models here.
from django.db import models

class OverlayMessage(models.Model):
    text = models.CharField(max_length=255, default="Ahoj")
    is_visible = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'Viditelné' if self.is_visible else 'Skryté'})"

class OverlayMessage(models.Model):
    text = models.CharField(max_length=255, default="Ahoj")
    is_visible = models.BooleanField(default=True)
    is_enabled = models.BooleanField(default=True)  # Nové pole pro zapínání/vypínání

    def __str__(self):
        return f"{self.text} (Visible: {self.is_visible}, Enabled: {self.is_enabled})"