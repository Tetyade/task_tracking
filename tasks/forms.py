from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'due_date']

class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [
        ('', 'All'),
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),]
    PRIORITY_CHOICES = [
        ('', 'All'),
        (1, '!!!'),
        (2, '!!'),
        (3, '!'),]

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label='Status')
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False, label='Priority')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['status'].widget.attrs.update({'class': 'form-control'})