from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.core.mixins import PageTitleMixin


class HomeView(PageTitleMixin, TemplateView):
    template_name = "core/home.html"
    page_title = "Home"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("inventory_list")
        return super().dispatch(request, *args, **kwargs)
