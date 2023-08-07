from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.core.paginator import Paginator,EmptyPage,InvalidPage

# Create your views here.
def allProdCategory(request, c_slug=None):
    c_page = None
    products = None
    if c_slug is not None:
        c_page = get_object_or_404(Category, slug=c_slug)
        product_list = Product.objects.all().filter(category=c_page, available=True)
    else:
        product_list = Product.objects.all().filter(available=True)
    paginator=Paginator(product_list,6)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1
    try:
        products=paginator.page(page)
    except (EmptyPage,InvalidPage):
        products=paginator.page(Paginator.num_pages)
    return render(request, 'category.html', {'category': c_page, 'products': products})


def proDetails(request, c_slug, pro_slug):
    try:
        product = Product.objects.get(category__slug=c_slug, slug=pro_slug)
    except Exception as e:
        raise e
    return render(request, 'product.html', {'product': product})
