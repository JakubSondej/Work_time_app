from django.urls import path
from . import views

urlpatterns = [
    path("entries/", views.work_entry_list, name="entries"),
]