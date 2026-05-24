from django import forms
from .models import WorkEntry

class WorkEntryForm(forms.ModelForm):
    class Meta:
        model = WorkEntry
        fields = [
            "date",
            "start_time",
            "end_time",
            "break_minutes",
            "description"
        ]