from django.urls import path
from django.shortcuts import redirect
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

    #import CSV
    path("reports/employee/csv/", views.export_employee_report_csv, name="export_employee_report_csv"),
    path("reports/manager/csv/", views.export_manager_report_csv, name="export_manager_report_csv"),
    
    path("entries/", lambda request: redirect("work_day_list")),
    path("entries/new/", lambda request: redirect("work_day_create")),

    #Exel reports
    path("reports/employee/xlsx/", views.export_employee_report_xlsx, name="export_employee_report_xlsx"),
    path("reports/manager/xlsx/", views.export_manager_report_xlsx, name="export_manager_report_xlsx"),
]