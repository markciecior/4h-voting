from django.http import HttpResponseRedirect
from django.urls import reverse


def login_required_fingerprint(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(
                f"{reverse('django_fingerprint:fplogin')}?next={request.path}"
            )
        response = view_func(request, *args, **kwargs)
        return response

    return wrapper
