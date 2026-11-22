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
