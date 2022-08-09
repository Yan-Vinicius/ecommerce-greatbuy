from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from store.models import Product
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def store(request, category_slug=None):

    categories = None
    products = None
    category = Category.objects.all()
    if category_slug is not None:

        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    else:

        products = Product.objects.all().filter(is_available=True)
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {'products': paged_products, 'product_count': product_count, 'categories': category}

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()

    except Exception as e:
        raise e

    context = {'product': product, 'in_cart': in_cart}

    return render(request, 'store/product_detail.html', context)


def search(request):

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            # Q serve para selecionar mais de um campo para fazer pesquisa
            # icontains serve para ver se a keyword está no campo que eu quero
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) |
                                                                        Q(product_name__icontains=keyword))
            product_count = products.count()

        context = {'products': products, 'product_count': product_count}

    return render(request, 'store/store.html', context)
