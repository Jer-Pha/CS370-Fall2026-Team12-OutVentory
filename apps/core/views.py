from django.views.generic import TemplateView

from apps.core.mixins import PageTitleMixin


class HomeView(PageTitleMixin, TemplateView):
    template_name = "core/home.html"
    page_title = "Home"
