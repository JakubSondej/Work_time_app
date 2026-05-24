from django.contrib import admin

# Register your models here:

from .models import WorkEntry

@admin.register(WorkEntry)
class WorkEntryAdmin(admin.ModelAdmin):
    # Kolumny, które będą widoczne na głównej liście wpisów:
    list_display = ('user', 'date', 'start_time', 'end_time', 'break_minutes', 'approved')
    
    # Filtry boczne, ułatwiające szukanie:
    list_filter = ('approved', 'date', 'user')
    
    # Pola, po których można wyszukiwać wpisy:
    search_fields = ('user__username', 'description')