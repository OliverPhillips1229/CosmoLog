from django.contrib import admin
from .models import Mission, Experiment

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'agency', 'launch_date', 'crewed', 'outcome')
    list_filter = ('agency', 'crewed', 'outcome')
    search_fields = ('name', 'agency')

@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'success_status')
    list_filter = ('category', 'success_status')
    search_fields = ('title',)