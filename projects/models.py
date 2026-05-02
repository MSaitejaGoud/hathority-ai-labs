"""
Data model for AI agent projects displayed on the showcase.

A single `Project` model powers both the homepage card grid and the
detail page. All content is managed via the Django Admin.
"""
from django.db import models


class Project(models.Model):
    # ----- Choices -----
    CATEGORY_CHOICES = [
        ("Boomi AI Agents", "Boomi AI Agents"),   # was "AI Agent" / "Automation"
        ("Boomi Agents", "Boomi Agents"),
        ("Active Agent", "Active Agent"),
        ("Other", "Other"),
    ]

    STATUS_CHOICES = [
        ("Completed", "Completed"),
        ("In Progress", "In Progress"),
        ("Live", "Live"),
        ("Planned", "Planned"),
    ]

    # ----- Fields -----
    title = models.CharField(max_length=100)
    short_description = models.CharField(
        max_length=200,
        help_text="1-2 line preview shown on project cards",
    )
    full_description = models.TextField()
    category = models.CharField(
        max_length=32,
        choices=CATEGORY_CHOICES,
        default="Boomi AI Agents",
    )
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default="Planned",
    )
    image = models.ImageField(
        upload_to="project_images/",
        blank=True,
        null=True,
        help_text="Optional cover image shown on the card and detail page",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self) -> str:
        return self.title
