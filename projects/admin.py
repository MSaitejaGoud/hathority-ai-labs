"""Django Admin configuration for the Project model."""
from django.contrib import admin
from django.utils.html import format_html

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "built_by", "created_at", "thumbnail")
    list_filter = ("category", "solution_type")
    search_fields = ("title", "short_description", "category", "built_by")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

    fieldsets = (
        ("Basic Info", {
            "fields": ("title", "short_description", "full_description", "key_features"),
        }),
        ("Classification", {

            "fields": ("category", "solution_type"),

        }),
        ("Credits & Dates", {
            "fields": ("built_by", "published_on"),
        }),
        ("Media", {
            "fields": ("image", "video_url"),
        }),
        ("Metadata", {
            "fields": ("created_at",),
        }),
    )

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:36px;border-radius:4px;" />',
                obj.image.url,
            )
        return "—"
    thumbnail.short_description = "Preview"
