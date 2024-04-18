from django.contrib import admin
from django.db import models
from .models import Pet, Profile

# Register your models here.
class PetAdmin(admin.ModelAdmin):
    list_display = ["name", "owner", "breed", "cutest_count", "unique_count", "people_choice_count"]
    list_filter = ["name", "owner", "breed"]

    def get_queryset(self, request):
        qs = super(PetAdmin, self).get_queryset(request)
        qs = qs.annotate(models.Count('unique'), models.Count('cutest'), models.Count('people_choice'), )
        return qs

    def cutest_count(self, obj):
        return obj.cutest__count
    cutest_count.admin_order_field = 'cutest__count'

    def unique_count(self, obj):
        return obj.unique__count
    unique_count.admin_order_field = 'unique__count'

    def people_choice_count(self, obj):
        return obj.people_choice__count
    people_choice_count.admin_order_field = 'people_choice__count'

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "vote_unique", "vote_cutest", "vote_people_choice"]
    list_filter = ["vote_unique", "vote_cutest", "vote_people_choice"]

admin.site.register(Pet, PetAdmin)
admin.site.register(Profile, ProfileAdmin)