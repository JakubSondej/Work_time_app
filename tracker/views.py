from urllib import request

from django.shortcuts import render

# Create your views here.
# from .models import WorkEntry

# def work_entry_list(request):
#     # Korzystamy z naszego managera, który sam decyduje co pokazać
#     entries = WorkEntry.objects.for_user(request.user)
#     return render(request, 'tracker/entry_list.html', {'entries': entries})


from .models import WorkEntry

def work_entry_list(request):

    user = request.user

    if user.groups.filter(name="Manager").exists() or user.is_superuser:
        entries = WorkEntry.objects.all()
    else:
        entries = WorkEntry.objects.filter(user=user)

    return render(request, "tracker/entry_list.html", {"entries": entries})
