from django.urls import path

from apps.users.views import (
    CompanyAdminSignUpView,
    EmployeeSignUpView,
    SignUpView,
)

urlpatterns = [
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
]
