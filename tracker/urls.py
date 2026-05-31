from django.urls import path
from . import views

urlpatterns = [
    path("work-days/", views.work_day_list, name="work_day_list"),
    path("work-days/new/", views.work_day_create, name="work_day_create"),

    # stare ścieżki możesz zostawić tymczasowo
    # path("entries/", views.work_entry_list, name="entries"),
    # path("entries/new/", views.work_entry_create, name="entry_create"),
]