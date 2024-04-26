from django import forms
from .models import Ballot, Pet


class BallotForm(forms.ModelForm):
    vote_unique = forms.ModelChoiceField(
        queryset=Pet.objects, empty_label=None, widget=forms.RadioSelect()
    )
    vote_cutest = forms.ModelChoiceField(
        queryset=Pet.objects, empty_label=None, widget=forms.RadioSelect()
    )
    vote_people_choice = forms.ModelChoiceField(
        queryset=Pet.objects, empty_label=None, widget=forms.RadioSelect()
    )

    class Meta:
        model = Ballot
        fields = ["vote_unique", "vote_cutest", "vote_people_choice"]
