from django.contrib import admin
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.db import models
from .models import Pet, Ballot, ManualBallot, Show, UserProfile

import pprint


# Register your models here.
@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "owner",
        "breed",
        "cutest_count",
        "unique_count",
        "people_choice_count",
        "show",
    ]
    list_filter = ["name", "owner", "breed", "show"]

    def get_queryset(self, request):
        qs = super(PetAdmin, self).get_queryset(request)
        qs = qs.annotate(
            models.Count("unique"),
            models.Count("cutest"),
            models.Count("people_choice"),
        )
        return qs

    @admin.display(ordering="cutest__count")
    def cutest_count(self, obj):
        return obj.cutest__count

    @admin.display(ordering="unique__count")
    def unique_count(self, obj):
        return obj.unique__count

    @admin.display(ordering="people_choice__count")
    def people_choice_count(self, obj):
        return obj.people_choice__count


@admin.register(Ballot)
class BallotAdmin(admin.ModelAdmin):
    list_display = ["user", "vote_unique", "vote_cutest", "vote_people_choice", "show"]
    list_filter = ["vote_unique", "vote_cutest", "vote_people_choice", "show"]


@admin.register(ManualBallot)
class ManualBallotAdmin(admin.ModelAdmin):
    list_display = ["vote_people_choice"]
    list_filter = ["vote_people_choice"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "date_joined", "user_agent", "ip_address"]
    list_filter = ["date_joined"]


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ["name", "date", "location", "active"]


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    def user(self, obj):
        session_user = obj.get_decoded().get("_auth_user_id")
        user = User.objects.get(pk=session_user)
        return user.email

    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace("\n", "<br>\n")

    list_display = ["user", "session_key", "_session_data", "expire_date"]
    readonly_fields = ["_session_data"]
