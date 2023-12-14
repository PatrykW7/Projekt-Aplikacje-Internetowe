from django.shortcuts import render
from django.db.models import Q
from aimodels.models import AiModel, Category

# Create your views here.


def all_models(request):
    categories = Category.objects.all()
    aimodels = AiModel.objects.all()

    active_category = request.GET.get("category", "")

    if active_category:
        aimodels = aimodels.filter(category__slug=active_category)

    query = request.GET.get("query", "")

    if query:
        aimodels = aimodels.filter(
            Q(name__icontains=query) | (Q(description__icontains=query))
        )

    context = {
        "categories": categories,
        "aimodels": aimodels,
        "active_category": active_category,
    }
    return render(request, "aimodels/all_models.html", context)


def aimodel(request, slug):
    aimodel = AiModel.objects.get(slug=slug)

    return render(request, "aimodels/aimodel.html", {"aimodel": aimodel})
