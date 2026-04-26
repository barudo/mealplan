from django.urls import path

from . import views

app_name = "mealplan"

urlpatterns = [
    path("", views.start, name="start"),
    path("questions/<int:number>/", views.question, name="question"),
    path("processing/", views.processing, name="processing"),
]
