from django.contrib import admin
from .models import Person,Catalog,Report
# Register your models here.

admin.site.register(Person)
admin.site.register(Catalog)
admin.site.register(Report)
