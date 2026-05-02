"""Django Admin configuration for the Project model."""
from django.contrib import admin
from django.utils.html import format_html

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # Columns shown in the changelist
    list_display = ("title", "category", "status", "created_at", "thumbnail")
    list_filter = ("category", "status")
    search_fields = ("title", "short_description", "category")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "short_description", "full_description"),
        }),
        ("Classification", {
            "fields": ("category", "status"),
        }),
        ("Media", {
            "fields": ("image",),
        }),
        ("Metadata", {
            "fields": ("created_at",),
        }),
    )

    def thumbnail(self, obj):
        """Render a small image preview in the admin changelist."""
        if obj.image:
            return format_html(
                '<img src="{}" style="height:36px;border-radius:4px;" />',
                obj.image.url,
            )
        return "—"
    thumbnail.short_description = "Preview"
