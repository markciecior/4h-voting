from collections import Counter
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.db.models import Count
from .forms import BallotForm, ManualBallotForm
from .models import Pet, Ballot, ManualBallot, Show
from django_thumbmark.decorators import login_required_thumbmark

import altair as alt
import pandas as pd
from datetime import datetime, timedelta


@login_required_thumbmark
def index(request):
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
            request.user.ballot.vote_people_choice = people_choice_pet
            request.user.ballot.save()
            messages.success(request, "Vote recorded!")
            return render(request, "voting4h/success.html", {})
        else:
            messages.warning(request, "Improper votes, please try again.")
            return render(
                request,
                "voting4h/index.html",
                {"user": request.user, "ballot_form": ballot_form},
            )

    else:
        ballot_form = BallotForm()
        user_agent = request.headers.get("user-agent", "")
        if request.user.userprofile.user_agent != user_agent:
            request.user.userprofile.user_agent = user_agent
            request.user.userprofile.save()
        if request.user.ballot.vote_people_choice is not None:
            messages.warning(
                request,
                "Your vote has already been recorded.  You may modify your vote below.",
            )
            ballot_form = BallotForm(
                initial={"vote_people_choice": request.user.ballot.vote_people_choice}
            )

    return render(
        request,
        "voting4h/index.html",
        {"user": request.user, "ballot_form": ballot_form},
    )


def manual(request):
    if request.method == "POST":
        ballot_form = ManualBallotForm(request.POST)
        if ballot_form.is_valid():
            # unique_pk = request.POST.get("vote_unique")
            # cutest_pk = request.POST.get("vote_cutest")
            people_choice_pk = request.POST.get("vote_people_choice")
            # unique_pet = Pet.objects.get(id=unique_pk)
            # cutest_pet = Pet.objects.get(id=cutest_pk)
            people_choice_pet = Pet.objects.get(id=people_choice_pk)
            # user.ballot.vote_unique = unique_pet
            # user.ballot.vote_cutest = cutest_pet
            ballot = ManualBallot()
            ballot.vote_people_choice = people_choice_pet
            # user.ballot.vote_people_choice = people_choice_pet
            ballot.save()
            messages.success(request, "Vote recorded!")
            return render(request, "voting4h/success.html", {})
        else:
            messages.warning(request, "Improper votes, please try again.")
            return render(
                request,
                "voting4h/manual.html",
                {"ballot_form": ballot_form},
            )
    else:
        ballot_form = BallotForm()

    return render(request, "voting4h/manual.html", {"ballot_form": ballot_form})


def results(request):
    results = (
        Ballot.objects.filter(show__active=True)
        .values("vote_people_choice__name")
        .annotate(total=Count("vote_people_choice"))
        .order_by("-total")
    )
    results2 = [{i["vote_people_choice__name"]: i["total"]} for i in results]
    results3 = {k: v for pet in results2 for k, v in pet.items()}
    manual_results = (
        ManualBallot.objects.filter(show__active=True)
        .values("vote_people_choice__name")
        .annotate(total=Count("vote_people_choice"))
        .order_by("-total")
    )
    manual_results2 = [
        {i["vote_people_choice__name"]: i["total"]} for i in manual_results
    ]
    manual_results3 = {k: v for pet in manual_results2 for k, v in pet.items()}
    results = dict(Counter(results3) + Counter(manual_results3))
    return render(
        request,
        "voting4h/results.html",
        {"results": sorted(results.items(), reverse=True)},
    )


def graph(request):
    return render(request, "voting4h/graph.html")


def api_graph1(request):
    retVal = Ballot.objects.filter(show__active=True).values(
        "user_id", "user__date_joined", "vote_people_choice__name"
    )
    df = pd.DataFrame.from_records(retVal).dropna(subset="vote_people_choice__name")
    df.rename(
        columns={"vote_people_choice__name": "Pet", "user__date_joined": "Date"},
        inplace=True,
    )

    chart = (
        alt.Chart(df, title="Votes by Pet")
        .mark_bar()
        .encode(
            x=alt.X("count(Pet)", title="Total Votes"),
            y=alt.Y("Pet", sort="-x", title="Pet"),
            color="Pet",
            tooltip=["count(Pet)"],
            order=alt.Order("count(Pet)", sort="descending"),
        )
        .properties(width=400)
    )
    return HttpResponse(chart.to_json(), content_type="application/json")


def api_graph2(request):
    retVal = Ballot.objects.filter(
        # user__date_joined__lte=datetime(2025, 7, 21, 14, 0),
        show__active=True,
    ).values("user_id", "user__date_joined", "vote_people_choice__name")
    df = pd.DataFrame.from_records(retVal).dropna(subset="vote_people_choice__name")
    df.rename(
        columns={"vote_people_choice__name": "Pet", "user__date_joined": "Date"},
        inplace=True,
    )

    chart = (
        alt.Chart(df, title="Votes over Time")
        .mark_bar(
            width=2,
        )
        .encode(
            x=alt.X("Date:T"),
            y=alt.Y("Pet:N"),
            color="Pet:N",
        )
        .properties(width=400)
    )
    return HttpResponse(chart.to_json(), content_type="application/json")


def api_graph3(request):
    retVal = Ballot.objects.filter(
        # user__date_joined__lte=datetime(2025, 7, 21, 14, 0),
        show__active=True,
    ).values("user_id", "user__date_joined", "vote_people_choice__name")
    df = pd.DataFrame.from_records(retVal).dropna(subset="vote_people_choice__name")
    df.rename(
        columns={"vote_people_choice__name": "Pet", "user__date_joined": "Date"},
        inplace=True,
    )

    chart = (
        alt.Chart(df, title="Cumulative Votes by Pet")
        .mark_circle(size=60)
        .transform_window(
            cumulative_count="count(Pet)", sort=[{"field": "Date"}], groupby=["Pet"]
        )
        .encode(
            x="Date:T",
            y=alt.Y("cumulative_count:Q"),
            color="Pet",
        )
        .properties(width=400)
    )
    return HttpResponse(chart.to_json(), content_type="application/json")


def api_graph4(request):
    retVal = Ballot.objects.filter(
        # user__date_joined__lte=datetime(2025, 7, 21, 14, 0),
        show__active=True,
    ).values("user_id", "user__date_joined", "vote_people_choice__name")
    df = pd.DataFrame.from_records(retVal).dropna(subset="vote_people_choice__name")
    df.rename(
        columns={"vote_people_choice__name": "Pet", "user__date_joined": "Date"},
        inplace=True,
    )

    chart = (
        alt.Chart(df, title="Cumulative Votes by Pet")
        .mark_area(opacity=0.3)
        .transform_window(
            cumulative_count="count(Pet)", sort=[{"field": "Date"}], groupby=["Pet"]
        )
        .encode(
            x=alt.X("Date:T"),
            y=alt.Y("cumulative_count:Q").stack(None),
            color="Pet:N",
        )
        .properties(width=400)
    )
    return HttpResponse(chart.to_json(), content_type="application/json")
