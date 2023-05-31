from django import forms
from .models import Task,Plan
from django.forms import ModelForm
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['plan', 'title', 'description', 'start_date', 'start_time', 'end_date', 'end_time']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = ['title', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError('End date cannot be before start date.')