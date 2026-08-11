from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import (
    ResearchProject,
    Resource,
    Summary,
    Citation,
    ComparisonTable,
    ComparisonRow,
    Subscription,
)
class ResearchProjectForm(forms.ModelForm):
    class Meta:
        model = ResearchProject
        fields = ["title", "topic", "description", "status"]

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter project title"}),
            "topic": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter project topic"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Describe the project"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ["title", "resource_type", "file", "external_url", "notes", "full_text"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter resource title"
            }),
            "resource_type": forms.Select(attrs={
                "class": "form-select"
            }),
            "file": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "external_url": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://example.com"
            }),
            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Add notes about this resource"
            }),
            "full_text": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Paste searchable text from the paper or resource here"
            }),
        }

class SummaryForm(forms.ModelForm):
    class Meta:
        model = Summary
        fields = ["title", "content"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter summary title"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 10,
                "placeholder": "Write your research summary here"
            }),
        }


class CitationForm(forms.ModelForm):
    class Meta:
        model = Citation
        fields = ["citation_text", "source_title", "source_url"]

        widgets = {
            "citation_text": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Enter citation text"
            }),
            "source_title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter source title"
            }),
            "source_url": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://example.com"
            }),
        }
class ComparisonTableForm(forms.ModelForm):
    class Meta:
        model = ComparisonTable
        fields = ["title", "description", "item_one", "item_two"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Comparison title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Optional description"}),
            "item_one": forms.TextInput(attrs={"class": "form-control", "placeholder": "Item A"}),
            "item_two": forms.TextInput(attrs={"class": "form-control", "placeholder": "Item B"}),
        }


class ComparisonRowForm(forms.ModelForm):
    class Meta:
        model = ComparisonRow
        fields = ["criterion", "item_one_value", "item_two_value", "order"]
        widgets = {
            "criterion": forms.TextInput(attrs={"class": "form-control", "placeholder": "Criterion"}),
            "item_one_value": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "item_two_value": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "order": forms.NumberInput(attrs={"class": "form-control"}),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter email"
        })
    )

    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter first name"
        })
    )

    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter last name"
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter username"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Enter password"
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm password"
        })

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ["user", "plan_name", "status", "start_date", "end_date", "is_archived"]

        widgets = {
            "user": forms.Select(attrs={
                "class": "form-select"
            }),
            "plan_name": forms.Select(attrs={
                "class": "form-select"
            }),
            "status": forms.Select(attrs={
                "class": "form-select"
            }),
            "start_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "end_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "is_archived": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ["user", "plan_name", "status", "start_date", "end_date", "is_archived"]

        widgets = {
            "user": forms.Select(attrs={
                "class": "form-select"
            }),
            "plan_name": forms.Select(attrs={
                "class": "form-select"
            }),
            "status": forms.Select(attrs={
                "class": "form-select"
            }),
            "start_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "end_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "is_archived": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }