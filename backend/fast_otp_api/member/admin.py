from django.contrib import admin
from .models import App, Config, Contact, OtpTimeline

# Register your models here.

@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ("id", "display_name", "label")
    list_editable = ("display_name", "label")

admin.site.register(OtpTimeline)


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "profile", "set_duration")
    list_editable = ["set_duration"]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    @admin.display(description="Name")
    def upper_case_name(self):
        return ("%s %s" %(self.first_name, self.last_name)).upper() #type: ignore

    list_display = ("id", upper_case_name, "phone_number", "label")
    list_editable = ["label"]

    