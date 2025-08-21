from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.UserRegistrationView.as_view(), name="user-registration"),
    path("", views.hello_world, name="hello-world"),
]