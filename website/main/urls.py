from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("sign-up/", views.sign_up, name="sing_up"),
    #path('login/', views.LoginView.as_view(template_name='core/login.html'), name = "login"),
]
