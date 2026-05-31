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


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

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