from django.db import models
from django.conf import settings

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('SEED', 'Seeds'),
        ('FERT', 'Fertilizer'),
        ('PEST', 'Pesticide'),
        ('TOOL', 'Tools/Equipment'),
        ('FEED', 'Animal Feed'),
        ('LIVE', 'Livestock'),
        ('CROP', 'Crops'),
        ('OTHER', 'Other'),
    ]

    UNIT_CHOICES = [
        ('KG', 'Kilograms'),
        ('G', 'Grams'),
        ('L', 'Liters'),
        ('ML', 'Milliliters'),
        ('UNIT', 'Units'),
        ('BAG', 'Bags'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=4, choices=UNIT_CHOICES)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Optional but useful fields
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expiry_date = models.DateField(null=True, blank=True)
    supplier = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)  # Storage location
    
    # Metadata
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = ['user', 'name']  # Prevent duplicate names per user

    def __str__(self):
        return f"{self.name} ({self.get_quantity_display()})"

    def get_quantity_display(self):
        return f"{self.quantity} {self.get_unit_display()}"

    def get_total_cost(self):
        return self.quantity * self.cost_per_unit

    def is_low_stock(self):
        return self.quantity <= self.minimum_stock 