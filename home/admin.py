from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models  import Person
from .models  import complainant
from .models  import women
# Register your models here.
@admin.register(Person)
class PersonAdmin(ImportExportModelAdmin):
    list_display = ('name','email','phone')

@admin.register(women)
class womenAdmin(ImportExportModelAdmin):
    list_display = ('crimeName','section','condition','age','punishment')

admin.site.register(complainant)