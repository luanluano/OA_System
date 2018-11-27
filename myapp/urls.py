from django.conf.urls import url
from django.contrib import admin

from myapp.views import RegisterAPI, LoginAPI, mylogout, send_verify_mail, verify

urlpatterns = [
    url(r'register$',RegisterAPI.as_view()),
    url(r"^login$", LoginAPI.as_view()),
    url(r"^logout$", mylogout),
    url(r"^send_mail$", send_verify_mail),
    url(r"^verify/(.*)", verify),
]