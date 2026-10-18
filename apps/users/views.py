from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from apps.core.mixins import PageTitleMixin
from apps.users.forms import (
    CompanyAdminRegistrationForm,
    EmployeeRegistrationForm,
)
from apps.users.mixins import AnonymousRequiredMixin


class SignUpView(AnonymousRequiredMixin, PageTitleMixin, TemplateView):
    template_name = "users/signup_home.html"
    page_title = "Sign Up"


class EmployeeSignUpView(AnonymousRequiredMixin, PageTitleMixin, CreateView):
    form_class = EmployeeRegistrationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    page_title = "Employee Sign Up"


class CompanyAdminSignUpView(
    AnonymousRequiredMixin, PageTitleMixin, CreateView
):
    form_class = CompanyAdminRegistrationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    page_title = "Owner Sign Up and Company Registration"
