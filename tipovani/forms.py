from django import forms
from .models import Kolo, Tip

class KoloForm(forms.ModelForm):
    class Meta:
        model = Kolo
        fields = ["zapasnik_a", "zapasnik_b"]

class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ["vybrany_team"]
        widgets = {
            "vybrany_team": forms.RadioSelect(choices=[('A', 'Tým A'), ('B', 'Tým B')])
        }