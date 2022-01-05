from django.contrib import admin
from . import models

class TagAdmin(admin.ModelAdmin):
    search_fields = ['tag']

admin.site.register(models.Tag, TagAdmin)
