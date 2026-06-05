import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User, Group
from tracker.models import UserProfile


def create_user(username, password, is_superuser=False, is_staff=False, group_name=None, hourly_rate="30.00"):
    user, created = User.objects.get_or_create(username=username)

    if created:
        user.set_password(password)

    user.is_superuser = is_superuser
    user.is_staff = is_staff
    user.save()

    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.hourly_rate = hourly_rate
    profile.save()

    if group_name:
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)


create_user(
    username="admin",
    password=os.environ.get("ADMIN_PASSWORD", "admin12345"),
    is_superuser=True,
    is_staff=True,
)

create_user(
    username="szef",
    password=os.environ.get("MANAGER_PASSWORD", "szef12345"),
    is_staff=True,
    group_name="Manager",
    hourly_rate="50.00",
)

create_user(
    username="pracownik",
    password=os.environ.get("EMPLOYEE_PASSWORD", "pracownik12345"),
    hourly_rate="30.00",
)

print("Initial users created.")