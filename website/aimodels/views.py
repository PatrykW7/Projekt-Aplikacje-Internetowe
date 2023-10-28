from django.shortcuts import render
from django.db.models import Q
from aimodels.models import AiModel, Category
# Create your views here.

def all_models(request):
    categories = Category.objects.all()
    products = AiModel.objects.all()
    
    # POBRANIE AKTYWNEGO ADRESU URL ZEBY WIEDZIEC KTORA NAZWE CATEGORY PODSWIETLAC 
    # category to jest iterator w petli z pliku shop

    # 'category' jest parametrem z .models import Product
    active_category = request.GET.get('category','')

    # FILTROWANIE PRODUKTOW, ZEBY WYSWIETLALY SIE TYLKO TE KTORE MAJA AKTYWNA KATEGORIE
    if active_category:
        products = products.filter(category__slug = active_category)

    # WYSZUKIWANIE WYBRANYCH PRODUKTOW PO NAZWIE PRODUKTU

    # query ODPOWIADA PARAMETROWI NAME Z INPUTA DO FILTROWANIA NAZW, '' OZNACZA ZE DOMYSLNIE JEST PUSTE
    query = request.GET.get('query', '')

    if query:
        products = products.filter(Q(name__icontains=query) | (Q(description__icontains=query)))

    context = {
        'categories': categories,
        'products': products,
        'active_category': active_category
    }
    return render(request, 'aimodels/all_models.html', context)