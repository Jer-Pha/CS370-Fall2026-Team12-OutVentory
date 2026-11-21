from django.contrib.auth.views import LoginView
from django.urls import path

from apps.users.views import (
    CompanyAdminSignUpView,
    EmployeeSignUpView,
    ManageEmployeePermissionsView,
    SignUpView,
)

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="registration/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("signup/", SignUpView.as_view(), name="signup"),
    path(
        "signup/employee/",
        EmployeeSignUpView.as_view(),
        name="signup_employee",
    ),
    path(
        "signup/owner/",
        CompanyAdminSignUpView.as_view(),
        name="signup_owner",
    ),
    path(
        "employees/",
        ManageEmployeePermissionsView.as_view(),
        name="employee_list",
    ),
]
