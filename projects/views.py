"""Views for the Team AI Showcase."""
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from .models import Project


DEFAULT_CATEGORY = "Boomi AI Agents"


def project_list(request):
    """
    Homepage view.

    Supports ?q= (search) and ?category= filtering — both applied together.
    Defaults to category="Boomi AI Agents" when no category param is given.
    Pass ?category=all to show every project.
    """
    query = request.GET.get("q", "").strip()
    # Use DEFAULT_CATEGORY when ?category= is absent; "all" means no filter
    category = request.GET.get("category", DEFAULT_CATEGORY).strip()

    projects = Project.objects.all()

    if category and category.lower() != "all":
        projects = projects.filter(category=category)

    if query:
        projects = projects.filter(
            Q(title__icontains=query)
            | Q(short_description__icontains=query)
            | Q(category__icontains=query)
        )

    projects = projects.order_by("-created_at")

    context = {
        "projects": projects,
        "query": query,
        "result_count": projects.count(),
        "active_category": category,  # passed to template for nav highlighting
    }
    return render(request, "projects/home.html", context)


def project_search_json(request):
    """Returns filtered projects as JSON for live search."""
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", DEFAULT_CATEGORY).strip()

    projects = Project.objects.all()
    if category and category.lower() != "all":
        projects = projects.filter(category=category)
    if query:
        projects = projects.filter(
            Q(title__icontains=query)
            | Q(short_description__icontains=query)
            | Q(category__icontains=query)
        )
    projects = projects.order_by("-created_at")

    data = [
        {
            "pk": p.pk,
            "title": p.title,
            "short_description": p.short_description,
            "category": p.category,
            "image_url": p.image.url if p.image else None,
        }
        for p in projects
    ]
    from django.http import JsonResponse
    return JsonResponse({"projects": data, "result_count": len(data), "query": query})


def project_detail(request, pk):
    """Detail page for a single project, looked up by primary key."""
    project = get_object_or_404(Project, pk=pk)
    features = []
    if project.key_features:
        for line in project.key_features.splitlines():
            line = line.strip()
            if not line:
                continue
            if ':' in line:
                title, _, desc = line.partition(':')
                features.append({"title": title.strip(), "desc": desc.strip()})
            else:
                features.append({"title": "", "desc": line})
    return render(request, "projects/project_detail.html", {"project": project, "features": features})
