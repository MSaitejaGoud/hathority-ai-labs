"""
Data migration: rename legacy category values to new labels.
  "AI Agent"    -> "Boomi AI Agents"
  "Automation"  -> "Boomi Agents"
"""
from django.db import migrations


def rename_categories(apps, schema_editor):
    Project = apps.get_model("projects", "Project")
    Project.objects.filter(category="AI Agent").update(category="Boomi AI Agents")
    Project.objects.filter(category="Automation").update(category="Boomi Agents")


def reverse_rename_categories(apps, schema_editor):
    Project = apps.get_model("projects", "Project")
    Project.objects.filter(category="Boomi AI Agents").update(category="AI Agent")
    Project.objects.filter(category="Boomi Agents").update(category="Automation")


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(rename_categories, reverse_rename_categories),
    ]
