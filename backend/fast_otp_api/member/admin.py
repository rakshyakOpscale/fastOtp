from django.contrib import admin
from .models import App, Config, Contact

# Register your models here.

admin.site.register(App)
admin.site.register(Config)
admin.site.register(Contact)
