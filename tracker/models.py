from django.db import models

# Create your models here:

from django.contrib.auth.models import User


# class WorkEntryManager(models.Manager):
#     def for_user(self, user):
#         if user.groups.filter(name='Szef').exists() or user.is_superuser:
#             return self.all()
#         return self.filter(user=user)

class WorkEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_minutes = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # objects = WorkEntryManager() # 

    def __str__(self):
        return f"{self.user.username} - {self.date}"