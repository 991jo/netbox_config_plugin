from django.contrib import admin

from .models import ConfigJob

@admin.register(ConfigJob)
class ConfigJobAdmin(admin.ModelAdmin):
    list_display = ("device", "config_status", "compare_status", "deployment_status")
