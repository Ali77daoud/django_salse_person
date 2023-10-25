from django.contrib import admin

from salesapp.models import Company, Salespeople, CommissionRate

# Register your models here.
admin.site.register(Company)
admin.site.register(Salespeople)
admin.site.register(CommissionRate)
