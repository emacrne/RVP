from django.db import models

class Tool(models.Model):
    id = models.CharField(primary_key=True, max_length=255, blank=True, null=False)
    barcode = models.CharField(max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    borrowed_by = models.CharField(max_length=255, blank=True, null=True)
    borrow_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.barcode} - {self.id}"

    class Meta:
        verbose_name = "Tool"
        verbose_name_plural = "Tools"