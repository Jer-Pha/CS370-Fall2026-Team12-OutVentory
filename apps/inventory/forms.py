from django import forms

from apps.inventory.models import Building


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ("name",)

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company:
            self.instance.company = company

    def clean_name(self):
        name = self.cleaned_data.get("name")
        company = getattr(self.instance, "company", None)

        if name and company:
            duplicates = Building.objects.filter(
                company=company, name__iexact=name
            )

            if self.instance.pk:
                duplicates = duplicates.exclude(pk=self.instance.pk)

            if duplicates.exists():
                raise forms.ValidationError(
                    "A building with this name already exists."
                )

        return name
