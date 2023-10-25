# Regions Model
from _decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


S, C, N, E, L = list(range(5))
REGIONS = (
    S, C, N, E, L,
)
REGION_CHOICES = (
    (S, "Southern Region"),
    (C, "Coastal Region"),
    (N, "Northern Region"),
    (E, "Eastern Region"),
    (L, "Lebanon Region"),
)


class Company(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)


class Salespeople(models.Model):
    name = models.CharField(max_length=255)
    number = models.IntegerField(unique=True)
    photo = models.FileField()
    main_region = models.IntegerField(choices=REGION_CHOICES)


class CommissionRate(models.Model):
    south_sales = models.DecimalField(decimal_places=3, max_digits=15)
    coast_sales = models.DecimalField(decimal_places=3, max_digits=15)
    north_sales = models.DecimalField(decimal_places=3, max_digits=15)
    east_sales = models.DecimalField(decimal_places=3, max_digits=15)
    lebanon_sales = models.DecimalField(decimal_places=3, max_digits=15)
    sales_people = models.ForeignKey(Salespeople, on_delete=models.CASCADE)
    total_commission = models.DecimalField(null=True, blank=True, decimal_places=3, max_digits=15)
    month = models.IntegerField(validators=[
        MinValueValidator(limit_value=1),
        MaxValueValidator(limit_value=12),
    ])
    year = models.IntegerField(validators=[
        MinValueValidator(limit_value=2000),
        MaxValueValidator(limit_value=2100),
    ])

    class Meta:
        unique_together = (
            ("sales_people", "month", "year")
        )

    def calculate_commission(self):
        sales = [
            self.south_sales,
            self.coast_sales,
            self.north_sales,
            self.east_sales,
            self.lebanon_sales,
        ]
        main_region_sales = sales.pop(self.sales_people.main_region)

        total_commission = 0
        for sale in sales:
            if sale <= 1000000:
                commission = sale * Decimal(0.03)
            else:
                commission_for_first_million = 1000000 * Decimal(0.03)
                commission_for_remaining = (sale - 1000000) * Decimal(0.04)
                commission = commission_for_first_million + commission_for_remaining
            total_commission += commission

        if main_region_sales <= 1000000:
            commission = main_region_sales * Decimal(0.05)
        else:
            commission_for_first_million = 1000000 * Decimal(0.05)
            commission_for_remaining = (main_region_sales - 1000000) * Decimal(0.07)
            commission = commission_for_first_million + commission_for_remaining
        total_commission += commission

        self.total_commission = total_commission
        self.save()
