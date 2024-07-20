from django import forms
from .models import Ballot, ManualBallot, Pet


class BallotForm(forms.ModelForm):
    # vote_unique = forms.ModelChoiceField(
    #     queryset=Pet.objects, empty_label=None, widget=forms.RadioSelect()
    # )
    # vote_cutest = forms.ModelChoiceField(
    #     queryset=Pet.objects, empty_label=None, widget=forms.RadioSelect()
    # )
    vote_people_choice = forms.ModelChoiceField(
        queryset=Pet.objects, empty_label=None, widget=forms.RadioSelect()
    )

    class Meta:
        model = Ballot
        fields = ["vote_people_choice"]


class ManualBallotForm(forms.ModelForm):
    # vote_unique = forms.ModelChoiceField(
    #     queryset=Pet.objects, empty_label=None, widget=forms.RadioSelect()
    # )
    # vote_cutest = forms.ModelChoiceField(
    #     queryset=Pet.objects, empty_label=None, widget=forms.RadioSelect()
    # )
    vote_people_choice = forms.ModelChoiceField(
        queryset=Pet.objects, empty_label=None, widget=forms.RadioSelect()
    )

    class Meta:
        model = ManualBallot
        fields = ["vote_people_choice"]
