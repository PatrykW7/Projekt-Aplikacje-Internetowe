from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from yt_sentiment.views import yt_sentiment
from aimodels.views import all_models
from aimodels.views import aimodel

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("sign-up/", views.sign_up, name="sing_up"),
    path("all_models/", all_models, name="all_models"),
    path("yt_sentiment/", yt_sentiment, name="yt_sentiment"),
    path('all_models/<slug:slug>/', aimodel, name = "aimodel"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
