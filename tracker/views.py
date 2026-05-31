import profile

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from decimal import Decimal
from django.contrib.auth.models import User

from .models import WorkDay
from .forms import WorkDayForm, WorkPeriodFormSet
import csv
from django.http import HttpResponse

@login_required
def work_day_list(request):
    user = request.user

    if user.groups.filter(name="Manager").exists() or user.is_superuser:
        days = WorkDay.objects.all()
    else:
        days = WorkDay.objects.filter(user=user)

    return render(request, "tracker/work_day_list.html", {"days": days})

@login_required
def work_day_create(request):
    if request.method == "POST":
        form = WorkDayForm(request.POST)
        formset = WorkPeriodFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            work_day = form.save(commit=False)
            work_day.user = request.user
            work_day.save()

            periods = formset.save(commit=False)
            for period in periods:
                period.work_day = work_day
                period.save()

            return redirect("work_day_list")
    else:
        form = WorkDayForm()
        formset = WorkPeriodFormSet()

    return render(request, "tracker/work_day_form.html", {
        "form": form,
        "formset": formset,
    })

@login_required
def work_day_update(request, pk):
    work_day = get_object_or_404(WorkDay, pk=pk)
    
    if work_day.approved and not is_manager(request.user):
        return redirect("work_day_list")

    if work_day.user != request.user and not request.user.groups.filter(name="Manager").exists() and not request.user.is_superuser:
        return redirect("work_day_list")

    if request.method == "POST":
        form = WorkDayForm(request.POST, instance=work_day)
        formset = WorkPeriodFormSet(request.POST, instance=work_day)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect("work_day_list")
    else:
        form = WorkDayForm(instance=work_day)
        formset = WorkPeriodFormSet(instance=work_day)

    return render(request, "tracker/work_day_form.html", {
        "form": form,
        "formset": formset,
    })

@login_required
def work_day_delete(request, pk):
    work_day = get_object_or_404(WorkDay, pk=pk)

    if work_day.approved and not is_manager(request.user):
        return redirect("work_day_list")

    if work_day.user != request.user and not request.user.groups.filter(name="Manager").exists() and not request.user.is_superuser:
        return redirect("work_day_list")

    if request.method == "POST":
        work_day.delete()
        return redirect("work_day_list")

    return render(request, "tracker/work_day_confirm_delete.html", {
        "work_day": work_day
    })  

@login_required
def monthly_summary(request):
    user = request.user

    today = date.today()

    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    #hourly_rate = Decimal("30.00")
    profile = getattr(user, "userprofile", None)

    if profile:
        hourly_rate = profile.hourly_rate
    else:
        hourly_rate = Decimal("30.00")
        


    if user.groups.filter(name="Manager").exists() or user.is_superuser:
        days = WorkDay.objects.filter(date__year=year, date__month=month)
    else:
        days = WorkDay.objects.filter(user=user, date__year=year, date__month=month)

    total_minutes = sum(day.total_minutes() for day in days)
    total_hours = Decimal(total_minutes) / Decimal(60)
    salary = total_hours * hourly_rate

    context = {
        "days": days,
        "year": year,
        "month": month,
        "total_minutes": total_minutes,
        "total_hours": round(total_hours, 2),
        "hourly_rate": hourly_rate,
        "salary": round(salary, 2),
    }

    return render(request, "tracker/monthly_summary.html", context)


def is_manager(user):
    return user.groups.filter(name="Manager").exists() or user.is_superuser

# @login_required
# def manager_dashboard(request):
#     if not is_manager(request.user):
#         return redirect("work_day_list")

#     today = date.today()
#     year = int(request.GET.get("year", today.year))
#     month = int(request.GET.get("month", today.month))

#     days = WorkDay.objects.filter(
#         date__year=year,
#         date__month=month
#     ).select_related("user").prefetch_related("periods")

#     total_minutes = sum(day.total_minutes() for day in days)

#     context = {
#         "days": days,
#         "year": year,
#         "month": month,
#         "total_minutes": total_minutes,
#         "total_hours": round(total_minutes / 60, 2),
#     }

#     return render(request, "tracker/manager_dashboard.html", context)

@login_required
def manager_dashboard(request):
    if not is_manager(request.user):
        return redirect("work_day_list")

    today = date.today()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))
    employee_id = request.GET.get("employee")

    days = WorkDay.objects.filter(
        date__year=year,
        date__month=month
    ).select_related("user").prefetch_related("periods")

    if employee_id:
        days = days.filter(user_id=employee_id)

    employees = User.objects.filter(
        workday__isnull=False
    ).distinct().order_by("username")

    total_minutes = sum(day.total_minutes() for day in days)

    context = {
        "days": days,
        "employees": employees,
        "selected_employee": employee_id,
        "year": year,
        "month": month,
        "total_minutes": total_minutes,
        "total_hours": round(total_minutes / 60, 2),
    }

    return render(request, "tracker/manager_dashboard.html", context)

@login_required
def approve_work_day(request, pk):
    if not is_manager(request.user):
        return redirect("work_day_list")

    work_day = get_object_or_404(WorkDay, pk=pk)

    if request.method == "POST":
        work_day.approved = True
        work_day.save()

    return redirect("manager_dashboard")


@login_required
def unapprove_work_day(request, pk):
    if not is_manager(request.user):
        return redirect("work_day_list")

    work_day = get_object_or_404(WorkDay, pk=pk)

    if request.method == "POST":
        work_day.approved = False
        work_day.save()

    return redirect("manager_dashboard")


def get_hourly_rate(user):
    profile = getattr(user, "userprofile", None)

    if profile:
        return profile.hourly_rate

    return Decimal("30.00")

@login_required
def export_employee_report_csv(request):
    user = request.user

    today = date.today()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    days = WorkDay.objects.filter(
        user=user,
        date__year=year,
        date__month=month
    ).prefetch_related("periods")

    hourly_rate = get_hourly_rate(user)
    total_minutes = sum(day.total_minutes() for day in days)
    total_hours = Decimal(total_minutes) / Decimal(60)
    salary = total_hours * hourly_rate

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="raport_{user.username}_{year}_{month}.csv"'

    response.write("\ufeff")

    writer = csv.writer(response, delimiter=";")

    writer.writerow(["Raport czasu pracy"])
    writer.writerow(["Pracownik", user.username])
    writer.writerow(["Miesiac", month])
    writer.writerow(["Rok", year])
    writer.writerow(["Stawka godzinowa", f"{hourly_rate} zl/h"])
    writer.writerow(["Lacznie godzin", f"{round(total_hours, 2)}"])
    writer.writerow(["Wynagrodzenie", f"{round(salary, 2)} zl"])
    writer.writerow([])

    writer.writerow(["Data", "Przedzialy", "Razem minut", "Razem godzin", "Status"])

    for day in days:
        periods = ", ".join(
            f"{p.start_time.strftime('%H:%M')}-{p.end_time.strftime('%H:%M')}"
            for p in day.periods.all()
        )

        day_minutes = day.total_minutes()
        day_hours = Decimal(day_minutes) / Decimal(60)

        writer.writerow([
            day.date,
            periods,
            day_minutes,
            round(day_hours, 2),
            "Zatwierdzone" if day.approved else "Oczekuje",
        ])

    return response

@login_required
def export_manager_report_csv(request):
    if not is_manager(request.user):
        return redirect("work_day_list")

    today = date.today()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))
    employee_id = request.GET.get("employee")

    days = WorkDay.objects.filter(
        date__year=year,
        date__month=month
    ).select_related("user").prefetch_related("periods")

    if employee_id:
        days = days.filter(user_id=employee_id)

    total_minutes = sum(day.total_minutes() for day in days)
    total_hours = Decimal(total_minutes) / Decimal(60)

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="raport_szefa_{year}_{month}.csv"'

    response.write("\ufeff")

    writer = csv.writer(response, delimiter=";")

    writer.writerow(["Raport czasu pracy - panel szefa"])
    writer.writerow(["Miesiac", month])
    writer.writerow(["Rok", year])
    writer.writerow(["Lacznie godzin", f"{round(total_hours, 2)}"])
    writer.writerow([])

    writer.writerow([
        "Pracownik",
        "Data",
        "Przedzialy",
        "Razem minut",
        "Razem godzin",
        "Status"
    ])

    for day in days:
        periods = ", ".join(
            f"{p.start_time.strftime('%H:%M')}-{p.end_time.strftime('%H:%M')}"
            for p in day.periods.all()
        )

        day_minutes = day.total_minutes()
        day_hours = Decimal(day_minutes) / Decimal(60)

        writer.writerow([
            day.user.username,
            day.date,
            periods,
            day_minutes,
            round(day_hours, 2),
            "Zatwierdzone" if day.approved else "Oczekuje",
        ])

    return response

