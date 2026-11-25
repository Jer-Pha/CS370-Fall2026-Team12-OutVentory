from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect


class AnonymousRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)


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
