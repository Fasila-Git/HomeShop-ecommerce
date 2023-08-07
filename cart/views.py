from django.shortcuts import render, redirect, get_object_or_404
from ecommerce_app.models import Product
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request, product_id):
    product=Product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(product=product,cart=cart,quantity=1)
        cart_item.save()
    return redirect('cart:cart_details')


def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1  # Decrement the quantity if it's greater than 1
            cart_item.save()
        else:
            cart_item.delete()
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        pass
    return redirect('cart:cart_details')

def delete_cart(request,product_id):
    prod=get_object_or_404(Product,id=product_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product_id,cart=cart)
        cart_item.delete()
    except:
        pass
    return redirect('cart:cart_details')

def cart_details(request,total=0,counter=0,cart_items=None):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request,"cart.html",dict(c_t=cart_items,cn=counter,tl=total))