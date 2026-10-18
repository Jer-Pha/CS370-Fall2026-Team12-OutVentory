from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from apps.users.forms import (
    CompanyAdminRegistrationForm,
    EmployeeRegistrationForm,
)


class SignUpView(TemplateView):
    template_name = "users/signup_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Sign Up"
        return context


class EmployeeSignUpView(CreateView):
    form_class = EmployeeRegistrationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Employee Sign Up"
        return context


class CompanyAdminSignUpView(CreateView):
    form_class = CompanyAdminRegistrationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Owner Sign Up and Company Registration"
        return context
