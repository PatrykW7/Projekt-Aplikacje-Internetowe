from django.shortcuts import render

# Create your views here.

def all_models(request):
    return render(request, "aimodels/all_models.html")