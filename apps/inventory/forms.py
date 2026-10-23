from django import forms

from apps.inventory.models import Building, Item, StorageLocation


class UniqueNameCompanyModelForm(forms.ModelForm):
    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company:
            self.instance.company = company

    def clean_name(self):
        name = self.cleaned_data.get("name")
        company = getattr(self.instance, "company", None)

        if name and company:
            model = self._meta.model
            duplicates = model.objects.filter(
                company=company, name__iexact=name
            )

            if self.instance.pk:
                duplicates = duplicates.exclude(pk=self.instance.pk)

            if duplicates.exists():
                verbose_name = model._meta.verbose_name.lower()
                raise forms.ValidationError(
                    f"{'An' if verbose_name[0] in 'aeiou' else 'A'}"
                    f" {verbose_name} with this name already exists."
                )

        return name


class BuildingForm(UniqueNameCompanyModelForm):
    class Meta:
        model = Building
        fields = ("name",)


class ItemForm(UniqueNameCompanyModelForm):
    class Meta:
        model = Item
        fields = ("name",)


class StorageLocationForm(forms.ModelForm):
    class Meta:
        model = StorageLocation
        fields = ("building", "name")

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company:
            self.fields["building"].queryset = Building.objects.filter(
                company=company
            )
