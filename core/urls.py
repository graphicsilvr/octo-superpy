from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"), # Matches the 'dashboard' function in views.py
]
