from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.edit import DeletionMixin


class CompanyMixin:
    company_lookup = "company"

    def get_company(self):
        return self.request.user.profile.company

    def get_queryset(self):
        lookup = {self.company_lookup: self.get_company()}
        return super().get_queryset().filter(**lookup)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if not isinstance(self, DeletionMixin):
            kwargs["company"] = self.get_company()
        return kwargs


class ProfilePermissionMixin(LoginRequiredMixin, UserPassesTestMixin):
    permission_required = None
    permission_match_any = False

    def get_permission_required(self):
        if self.permission_required is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} is missing the 'permission_required' attribute."
            )
        if isinstance(self.permission_required, str):
            return (self.permission_required,)
        return tuple(self.permission_required)

    def test_func(self):
        profile = getattr(self.request.user, "profile", None)

        if not profile:
            return False

        perms = self.get_permission_required()
        if self.permission_match_any:
            return any(getattr(profile, perm, False) for perm in perms)
        return all(getattr(profile, perm, False) for perm in perms)
