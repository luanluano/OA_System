from django.conf.urls import url
from django.contrib import admin

from myapp.views import RegisterAPI

urlpatterns = [
    url(r'register$',RegisterAPI.as_view())
]