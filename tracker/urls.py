from django.urls import path
from . import views

urlpatterns = [
    path("work-days/", views.work_day_list, name="work_day_list"),
    path("work-days/new/", views.work_day_create, name="work_day_create"),
    path("work-days/<int:pk>/edit/", views.work_day_update, name="work_day_update"),
    path("work-days/<int:pk>/delete/", views.work_day_delete, name="work_day_delete"),
    path("monthly-summary/", views.monthly_summary, name="monthly_summary"),

    #manager views
    path("manager/", views.manager_dashboard, name="manager_dashboard"),
    path("manager/<int:pk>/approve/", views.approve_work_day, name="approve_work_day"),
    path("manager/<int:pk>/unapprove/", views.unapprove_work_day, name="unapprove_work_day"),

    # stare ścieżki możesz zostawić tymczasowo
    # path("entries/", views.work_entry_list, name="entries"),
    # path("entries/new/", views.work_entry_create, name="entry_create"),
]