from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'priority', 'category', 'created_at', 'updated_at')
    list_filter = ('status', 'priority', 'category')
    search_fields = ('title', 'content')

    def save_model(self, request, obj, form, change):
        if not change:  
            obj.user = request.user
        super().save_model(request, obj, form, change)
