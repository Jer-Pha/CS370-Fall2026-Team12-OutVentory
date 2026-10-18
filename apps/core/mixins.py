class PageTitleMixin:
    page_title = ""

    def get_page_title(self):
        """Override this method if the title needs to be dynamic."""
        return self.page_title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = self.get_page_title()
        return context
