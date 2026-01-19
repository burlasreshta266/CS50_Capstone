from django.contrib import admin
from .models import Task, Project, Technology

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Technology)