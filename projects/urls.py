"""URL routes for the projects app."""
from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.project_list, name="home"),
    path("project/<int:pk>/", views.project_detail, name="detail"),
]
