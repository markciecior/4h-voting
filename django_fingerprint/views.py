from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import get_user_model, login
from django.urls import reverse


def fp(request):
    next = request.session.get("next")
    if not request.user.is_authenticated:
        fpid = request.GET.get("fpid")
        UserModel = get_user_model()
        user, _ = UserModel.objects.get_or_create(
            username=fpid,
            defaults={"username": fpid, "first_name": "Test", "last_name": "User"},
        )
        login(request, user)
    return JsonResponse({"url": next})


def fplogin(request):
    next = request.GET.get("next")
    fingerprint_url = reverse("django_fingerprint:fp")
    request.session["next"] = next
    return render(request, "django_fingerprint/login.html", {"fp_url": fingerprint_url})
