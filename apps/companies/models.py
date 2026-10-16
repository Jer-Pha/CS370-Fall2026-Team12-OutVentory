from django.db import models
from django.db.models.functions import Lower


class Company(models.Model):
    name = models.CharField(max_length=255, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="unique_lower_company_name",
                violation_error_message="A company with this name already exists.",
            )
        ]

    def __str__(self):
        return self.name

    @property
    def owner(self):
        return self.employees.filter(is_owner=True).first()
