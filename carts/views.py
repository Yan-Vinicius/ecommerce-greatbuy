from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from carts.models import Cart, CartItem
from store.models import Product, Variation


# Create your views here.
# Adicionar um _ antes de uma função faz ela se tornar privada
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()

    return  cart


def add_to_cart(request, product_id):

    product = Product.objects.get(id=product_id)
    product_variation = []

    if request.method == 'POST':
        #esse for serve para checar todas as infos que virão no POST
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                  variation_value__iexact=value)
                product_variation.append(variation)

            except:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))

    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))

    cart.save()

    cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

    if cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)

        # variações existentes -> banco de dados
        # variação atual -> product_variation
        # item_id -> banco de dados
        existing_var_list = []
        list_id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            existing_var_list.append(list(existing_variation))
            list_id.append(item.id)

        if product_variation in existing_var_list:
            index = existing_var_list.index(product_variation)
            item_id = list_id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()

        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)

            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)

            item.save()

    else:

        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)

        cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):

    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)

    try:

        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    except:
        pass

    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):

    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)

    cart_item.delete()

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

    except ObjectDoesNotExist:
        pass

    context = {'total': total, 'quantity': quantity, 'cart_items': cart_items}

    return render(request, 'store/cart.html', context)

