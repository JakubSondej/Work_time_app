# from django.db import models

# # Create your models here:

# from django.contrib.auth.models import User


# # class WorkEntryManager(models.Manager):
# #     def for_user(self, user):
# #         if user.groups.filter(name='Szef').exists() or user.is_superuser:
# #             return self.all()
# #         return self.filter(user=user)

# class WorkEntry(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     date = models.DateField()
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     break_minutes = models.IntegerField(default=0)
#     description = models.TextField(blank=True)
#     approved = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     # objects = WorkEntryManager() # 

#     def __str__(self):
#         return f"{self.user.username} - {self.date}"



from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User


class WorkDay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField(blank=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    def total_minutes(self):
        total = 0
        for period in self.periods.all():
            total += period.duration_minutes()
        return total

    def total_hours_display(self):
        minutes = self.total_minutes()
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}h {mins}min"


class WorkPeriod(models.Model):
    work_day = models.ForeignKey(
        WorkDay,
        on_delete=models.CASCADE,
        related_name="periods"
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"

    def duration_minutes(self):
        start = datetime.combine(self.work_day.date, self.start_time)
        end = datetime.combine(self.work_day.date, self.end_time)

        if end < start:
            end = end.replace(day=end.day + 1)

        diff = end - start
        minutes = int(diff.total_seconds() // 60)

        if minutes < 0:
            raise ValueError(f"End time ({self.end_time}) must be after start time ({self.start_time})")

        return minutes


# Stary model zostawiamy tymczasowo, żeby nie mieszać migracji.
class WorkEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_minutes = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=30.00)

    def __str__(self):
        return f"{self.user.username} profile"