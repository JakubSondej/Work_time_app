# from django import forms
# from .models import WorkEntry

# class WorkEntryForm(forms.ModelForm):
#     class Meta:
#         model = WorkEntry
#         fields = [
#             "date",
#             "start_time",
#             "end_time",
#             "break_minutes",
#             "description"
#         ]

from django import forms
from django.forms import inlineformset_factory

from .models import WorkDay, WorkPeriod


class WorkDayForm(forms.ModelForm):
    class Meta:
        model = WorkDay
        fields = ["date", "description"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class WorkPeriodForm(forms.ModelForm):
    class Meta:
        model = WorkPeriod
        fields = ["start_time", "end_time"]
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "end_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
        }


WorkPeriodFormSet = inlineformset_factory(
    WorkDay,
    WorkPeriod,
    form=WorkPeriodForm,
    extra=1,
    can_delete=True,
)