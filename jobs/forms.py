from django import forms
from .models import Application, Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "description", "company", "location", "salary"]
        
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["resume"]
        widgets = {
            "resume": forms.ClearableFileInput(attrs={"class": "form-control"})
        }