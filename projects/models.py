"""
Data model for AI agent projects displayed on the showcase.

A single `Project` model powers both the homepage card grid and the
detail page. All content is managed via the Django Admin.
"""
import base64
import re
from django.db import models


class Project(models.Model):
    # ----- Choices -----
    CATEGORY_CHOICES = [
        ("Boomi AI Agents", "Boomi AI Agents"),
        ("Hathority In-House Agents", "Hathority In-House Agents"),
        ("Active Engagements", "Active Engagements"),
        ("Other", "Other"),
    ]

    SOLUTION_TYPE_CHOICES = [
        ("Accelerator", "Accelerator"),
        ("Agents", "Agents"),
        ("AI Agent Accelerator", "AI Agent Accelerator"),
        ("AI Agent Recipe", "AI Agent Recipe"),
        ("Designer Agent Accelerator", "Designer Agent Accelerator"),
        ("Designer Agent Recipe", "Designer Agent Recipe"),
        ("Recipe", "Recipe"),
        ("Task Automation", "Task Automation"),
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
    built_by = models.CharField(
        max_length=100,
        default="HATHORITY | Partner",
        help_text="Name of the person or team who built this agent",
    )
    solution_type = models.CharField(
        max_length=30,
        choices=SOLUTION_TYPE_CHOICES,
        blank=True,
        null=True,
    )
    published_on = models.DateField(
        blank=True,
        null=True,
        help_text="Date this agent was published",
    )
    key_features = models.TextField(
        blank=True,
        null=True,
        help_text="One feature per line in format 'Title : Description'. Each line becomes a bullet point.",
    )
    image = models.ImageField(
        upload_to="project_images/",
        blank=True,
        null=True,
        help_text="Optional cover image shown on the card and detail page",
    )
    video_url = models.URLField(
        blank=True,
        null=True,
        help_text="Paste a Google Drive or OneDrive share link here",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self) -> str:
        return self.title

    def get_embed_url(self):
        """Convert any Google Drive or OneDrive share URL to an embeddable iframe URL."""
        url = self.video_url
        if not url:
            return None

        # Google Drive: swap /view or /edit with /preview
        if "drive.google.com/file/d/" in url:
            return re.sub(r"/(view|edit|share)[^/]*$", "/preview", url)

        # Already an embed URL — return as-is
        if "embed" in url:
            return url

        # OneDrive/SharePoint share links
        if "1drv.ms" in url or "onedrive.live.com" in url or "sharepoint.com" in url:
            encoded = base64.b64encode(url.encode("utf-8")).decode("utf-8")
            encoded = encoded.rstrip("=").replace("+", "-").replace("/", "_")
            return f"https://onedrive.live.com/embed?resid={encoded}&authkey=&em=2"

        return url
