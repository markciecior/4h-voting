"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from voting4h import views
from django.urls import path

from django_thumbmark.views import DjTmLoginView, DjTmScriptView

app_name = "voting4h"
urlpatterns = [
    path("results/", views.results, name="results"),
    path("graph/", views.graph, name="graph"),
    path("apigraph1/", views.api_graph1, name="apigraph1"),
    path("apigraph2/", views.api_graph2, name="apigraph2"),
    path("apigraph3/", views.api_graph3, name="apigraph3"),
    path("apigraph4/", views.api_graph4, name="apigraph4"),
    path("manual/", views.manual, name="manual"),
    path("tm/", DjTmScriptView.as_view(), name="tm"),
    path("login/", DjTmLoginView.as_view(), name="tmlogin"),
    path("", views.index, name="index"),
]
