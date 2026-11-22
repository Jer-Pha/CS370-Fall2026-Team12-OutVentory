from django.forms import modelformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from apps.companies.mixins import CompanyMixin
from apps.core.mixins import PageTitleMixin
from apps.users.forms import (
    CompanyAdminRegistrationForm,
    EmployeePermissionForm,
    EmployeeRegistrationForm,
)
from apps.users.mixins import AnonymousRequiredMixin, ProfilePermissionMixin
from apps.users.models import EmployeeProfile


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


class ManageEmployeePermissionsView(
    ProfilePermissionMixin, CompanyMixin, PageTitleMixin, ListView
):
    permission_required = (
        "is_owner",
        "is_admin",
    )
    permission_match_any = True
    model = EmployeeProfile
    context_object_name = "employees"
    page_title = "Manage Employee Permissions"
    template_name = "users/employee_list.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            # .exclude(user=self.request.user)
            .order_by("-is_owner", "-is_admin", "last_name", "first_name")
        )

    def get_formset(self, queryset=None, data=None):
        PermissionFormSet = modelformset_factory(
            EmployeeProfile,
            form=EmployeePermissionForm,
            extra=0,
            can_delete=False,
        )
        if queryset is None:
            queryset = self.get_queryset()

        return PermissionFormSet(
            data=data,
            queryset=queryset,
            form_kwargs={"request_user_profile": self.request.user.profile},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = self.get_formset()
        return context

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy("employee_list"))

        context = self.get_context_data()
        context["formset"] = formset
        return self.render_to_response(context)
