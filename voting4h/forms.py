from django import forms
from .models import Pet

class UniqueForm(forms.Form):
    ANIMAL_CHOICES = {
        p.pk: f"{p.name} ({p.breed}) by {p.owner}" for p in Pet.objects.all()
    }

    animal = forms.ChoiceField(choices=ANIMAL_CHOICES, required=True, label="Most Unique Pet", widget=forms.RadioSelect())

class PeopleChoiceForm(forms.Form):
    ANIMAL_CHOICES = {
        p.pk: f"{p.name} ({p.breed}) by {p.owner}" for p in Pet.objects.all()
    }

    animal = forms.ChoiceField(choices=ANIMAL_CHOICES, required=True, label="People's Choice Pet", widget=forms.RadioSelect)

class CutestForm(forms.Form):
    ANIMAL_CHOICES = {
        p.pk: f"{p.name} ({p.breed}) by {p.owner}" for p in Pet.objects.all()
    }

    animal = forms.ChoiceField(choices=ANIMAL_CHOICES, required=True, label="Cutest Pet", widget=forms.RadioSelect)
