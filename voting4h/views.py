from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib import messages
from .forms import UniqueForm, PeopleChoiceForm, CutestForm
from .models import Pet
import uuid

def index(request):
    User = get_user_model()
    user_id = request.session.get("user", None)
    if not user_id:
        user = User(first_name="Test", last_name="User", username=uuid.uuid4())
        user.save()
        request.session["user"] = user.pk
    else:
        user = User.objects.get(pk=user_id)
    
    if request.method == "POST":
        unique_form = UniqueForm(request.POST, prefix="unique_form")
        cutest_form = CutestForm(request.POST, prefix="cutest_form")
        people_choice_form = PeopleChoiceForm(request.POST, prefix="people_choice_form")
        if unique_form.is_valid() and people_choice_form.is_valid() and cutest_form.is_valid():
            unique_pk = request.POST.get("unique_form-animal")
            cutest_pk = request.POST.get("cutest_form-animal")
            people_choice_pk = request.POST.get("people_choice_form-animal")
            unique_pet = Pet.objects.get(id=unique_pk)
            cutest_pet = Pet.objects.get(id=cutest_pk)
            people_choice_pet = Pet.objects.get(id=people_choice_pk)
            user.profile.vote_unique = unique_pet
            user.profile.vote_cutest = cutest_pet
            user.profile.vote_people_choice = people_choice_pet
            user.profile.save()
            messages.success(request, "Vote recorded!")
            return render(
                request,
                "voting4h/success.html",
                {}
            )
        else:
            messages.warning(request, "Improper votes, please try again.")
            return render(
                request,
                "voting4h/index.html",
                {
                    "user": user,
                    "unique_form": unique_form,
                    "people_choice_form": people_choice_form,
                    "cutest_form": cutest_form,
                }
            )
    
    else:
        unique_form = UniqueForm(prefix="unique_form")
        people_choice_form = PeopleChoiceForm(prefix="people_choice_form")
        cutest_form = CutestForm(prefix="cutest_form")
        if user.profile.vote_cutest != None:
            messages.warning(request, "Your vote has already been recorded.  You may modify your vote below.")

    return render(
        request,
        "voting4h/index.html",
        {
            "user": user,
            "unique_form": unique_form,
            "people_choice_form": people_choice_form,
            "cutest_form": cutest_form,
        }
    )
