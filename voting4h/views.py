from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Count
from .forms import BallotForm
from .models import Pet, Ballot
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
        ballot_form = BallotForm(request.POST)
        if ballot_form.is_valid():
            # unique_pk = request.POST.get("vote_unique")
            # cutest_pk = request.POST.get("vote_cutest")
            people_choice_pk = request.POST.get("vote_people_choice")
            # unique_pet = Pet.objects.get(id=unique_pk)
            # cutest_pet = Pet.objects.get(id=cutest_pk)
            people_choice_pet = Pet.objects.get(id=people_choice_pk)
            # user.ballot.vote_unique = unique_pet
            # user.ballot.vote_cutest = cutest_pet
            user.ballot.vote_people_choice = people_choice_pet
            user.ballot.save()
            messages.success(request, "Vote recorded!")
            return render(request, "voting4h/success.html", {})
        else:
            messages.warning(request, "Improper votes, please try again.")
            return render(
                request,
                "voting4h/index.html",
                {"user": user, "ballot_form": ballot_form},
            )

    else:
        ballot_form = BallotForm()
        if user.ballot.vote_people_choice is not None:
            messages.warning(
                request,
                "Your vote has already been recorded.  You may modify your vote below.",
            )
            ballot_form = BallotForm(
                initial={"vote_people_choice": user.ballot.vote_people_choice}
            )

    return render(
        request, "voting4h/index.html", {"user": user, "ballot_form": ballot_form}
    )


def results(request):
    results = (
        Ballot.objects.all()
        .values("vote_people_choice__name")
        .annotate(total=Count("vote_people_choice"))
        .order_by("-total")
    )
    return render(request, "voting4h/results.html", {"results": results})
