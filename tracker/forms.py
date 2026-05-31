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
from django.core.exceptions import ValidationError
from django.utils import timezone
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

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > timezone.now().date():
            raise ValidationError("Data nie może być w przyszłości. Możesz dodać dzień pracy tylko dla przeszłych lub dzisiejszych dni.")
        return date


class WorkPeriodForm(forms.ModelForm):
    class Meta:
        model = WorkPeriod
        fields = ["start_time", "end_time"]
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "end_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if not start_time or not end_time:
            return cleaned_data

        if end_time <= start_time:
            if start_time.hour > end_time.hour:
                return cleaned_data
            else:
                raise ValidationError(
                    f"Godzina końca ({end_time.strftime('%H:%M')}) musi być po godzinie startu ({start_time.strftime('%H:%M')}). "
                    f"Jeśli praca trwa do następnego dnia (np. 18:00 - 02:00), będzie obsługiwana automatycznie."
                )

        return cleaned_data


class BaseWorkPeriodFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        periods = []
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                periods.append((
                    form.cleaned_data['start_time'],
                    form.cleaned_data['end_time']
                ))

        for i, (start1, end1) in enumerate(periods):
            for start2, end2 in periods[i+1:]:
                if not (end1 <= start2 or end2 <= start1):
                    raise ValidationError(
                        f"Przedziały czasowe się nakładają: "
                        f"{start1.strftime('%H:%M')}-{end1.strftime('%H:%M')} "
                        f"i {start2.strftime('%H:%M')}-{end2.strftime('%H:%M')}"
                    )


WorkPeriodFormSet = inlineformset_factory(
    WorkDay,
    WorkPeriod,
    form=WorkPeriodForm,
    formset=BaseWorkPeriodFormSet,
    extra=1,
    can_delete=True,
)