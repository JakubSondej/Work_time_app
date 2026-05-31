# from django.contrib import admin

# # Register your models here:

# from .models import WorkEntry

# @admin.register(WorkEntry)
# class WorkEntryAdmin(admin.ModelAdmin):
#     # Kolumny, które będą widoczne na głównej liście wpisów:
#     list_display = ('user', 'date', 'start_time', 'end_time', 'break_minutes', 'approved')
    
#     # Filtry boczne, ułatwiające szukanie:
#     list_filter = ('approved', 'date', 'user')
    
#     # Pola, po których można wyszukiwać wpisy:
#     search_fields = ('user__username', 'description')

from django.contrib import admin
from .models import WorkEntry, WorkDay, WorkPeriod, UserProfile

class WorkPeriodInline(admin.TabularInline):
    model = WorkPeriod
    extra = 1


@admin.register(WorkDay)
class WorkDayAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "approved", "created_at")
    list_filter = ("user", "date", "approved")
    search_fields = ("user__username",)
    inlines = [WorkPeriodInline]


@admin.register(WorkPeriod)
class WorkPeriodAdmin(admin.ModelAdmin):
    list_display = ("work_day", "start_time", "end_time")


@admin.register(WorkEntry)
class WorkEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "start_time", "end_time", "break_minutes", "approved")

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "hourly_rate")