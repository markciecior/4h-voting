from django.contrib import admin
from django.db import models
from .models import Pet, Profile


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
    ]
    list_filter = ["name", "owner", "breed"]

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


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "vote_unique", "vote_cutest", "vote_people_choice"]
    list_filter = ["vote_unique", "vote_cutest", "vote_people_choice"]
