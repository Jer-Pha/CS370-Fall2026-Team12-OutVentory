from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class OwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        profile = getattr(self.request.user, "profile", None)
        return bool(profile and profile.is_owner)


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        profile = getattr(self.request.user, "profile", None)
        return bool(profile and profile.is_admin)


class CompanyQuerySetMixin:
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(company=self.request.user.profile.company)
        )
