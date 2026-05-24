from django.shortcuts import render
from .models import WorkEntry
from .forms import WorkEntryForm
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required

# Create your views here.
# from .models import WorkEntry

# def work_entry_list(request):
#     # Korzystamy z naszego managera, który sam decyduje co pokazać
#     entries = WorkEntry.objects.for_user(request.user)
#     return render(request, 'tracker/entry_list.html', {'entries': entries})
@login_required
def work_entry_list(request):

    user = request.user
    if user.groups.filter(name="Manager").exists() or user.is_superuser:
        entries = WorkEntry.objects.all()
    else:
        entries = WorkEntry.objects.filter(user=user)

    return render(request, "tracker/entry_list.html", {"entries": entries})

@login_required
def work_entry_create(request):
    if request.method == "POST":
        form = WorkEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect("entries")
    else:
        form = WorkEntryForm()

    return render(request, "tracker/entry_form.html", {"form": form})