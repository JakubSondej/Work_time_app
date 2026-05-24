from django.urls import path
from . import views

urlpatterns = [
    path("entries/", views.work_entry_list, name="entries"),
    path("entries/new/", views.work_entry_create, name="entry_create"),

]