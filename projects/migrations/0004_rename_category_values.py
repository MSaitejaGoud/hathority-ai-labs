from django.db import migrations


def rename_categories(apps, schema_editor):
    Project = apps.get_model("projects", "Project")
    Project.objects.filter(category="Boomi Agents").update(category="Hathority In-House Agents")
    Project.objects.filter(category="Active Agent").update(category="Active Engagements")


def reverse_rename_categories(apps, schema_editor):
    Project = apps.get_model("projects", "Project")
    Project.objects.filter(category="Hathority In-House Agents").update(category="Boomi Agents")
    Project.objects.filter(category="Active Engagements").update(category="Active Agent")


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0003_alter_project_category"),
    ]

    operations = [
        migrations.RunPython(rename_categories, reverse_rename_categories),
    ]
