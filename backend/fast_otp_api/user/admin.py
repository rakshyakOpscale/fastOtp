from django.contrib import admin

from .models import Profile

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    @admin.display(description="Name")
    def upper_case_name(obj):
        return ("%s %s" % (obj.first_name, obj.last_name)).upper()  # type: ignore

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].disabled = True
        return form

    list_display = ("id", "user", upper_case_name)
