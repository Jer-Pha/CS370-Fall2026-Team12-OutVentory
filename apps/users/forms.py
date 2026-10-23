from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from apps.companies.models import Company
from apps.users.models import EmployeeProfile, User


class EmployeeRegistrationForm(UserCreationForm):
    # User Fields
    email = forms.EmailField()
    username = None

    # EmployeeProfile Fields
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(), required=True
    )

    class Meta:
        model = User
        fields = ("email",)

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=commit)

        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        company = self.cleaned_data["company"]

        if commit:
            EmployeeProfile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                company=company,
            )
        return user


class CompanyAdminRegistrationForm(UserCreationForm):
    # User field
    email = forms.EmailField(required=True)
    username = None

    # EmployeeProfile Fields
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    # Company Field
    company_name = forms.CharField(
        max_length=255, required=True, label="Company Name"
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_company_name(self):
        name = self.cleaned_data["company_name"].strip()
        if Company.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError(
                "A company with this name already exists."
            )
        return name

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=commit)

        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        company_name = self.cleaned_data["company_name"]

        if commit:
            company = Company.objects.create(name=company_name)

            EmployeeProfile.objects.create(
                user=user,
                company=company,
                first_name=first_name,
                last_name=last_name,
                is_owner=True,
            )

        return user
