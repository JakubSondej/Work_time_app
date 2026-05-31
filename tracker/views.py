# from django.shortcuts import render
# from .models import WorkEntry
# from .forms import WorkEntryForm
# from django.shortcuts import redirect

# from django.contrib.auth.decorators import login_required

# # Create your views here.
# # from .models import WorkEntry

# # def work_entry_list(request):
# #     # Korzystamy z naszego managera, który sam decyduje co pokazać
# #     entries = WorkEntry.objects.for_user(request.user)
# #     return render(request, 'tracker/entry_list.html', {'entries': entries})
# @login_required
# def work_entry_list(request):

#     user = request.user
#     if user.groups.filter(name="Manager").exists() or user.is_superuser:
#         entries = WorkEntry.objects.all()
#     else:
#         entries = WorkEntry.objects.filter(user=user)

#     return render(request, "tracker/entry_list.html", {"entries": entries})

# @login_required
# def work_entry_create(request):
#     if request.method == "POST":
#         form = WorkEntryForm(request.POST)
#         if form.is_valid():
#             entry = form.save(commit=False)
#             entry.user = request.user
#             entry.save()
#             return redirect("entries")
#     else:
#         form = WorkEntryForm()

#     return render(request, "tracker/entry_form.html", {"form": form})


import profile

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from decimal import Decimal

from .models import WorkDay
from .forms import WorkDayForm, WorkPeriodFormSet


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