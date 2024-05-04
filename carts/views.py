from django.shortcuts import render, redirect, get_object_or_404
from store.models import Book
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required



# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()
        cart = request.session.session_key
    return cart

def add_cart(request, product_id):
    current_user = request.user
    # print(current_user)
    product = Book.objects.get(id=product_id) #get the product
    # If the user is authenticated
    if current_user.is_authenticated:
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            # cart_item = CartItem.objects.filter(product=product)


            item = CartItem.objects.create(product=product, quantity=1, user=current_user)
            # item = CartItem.objects.create(product=product, quantity=1)
            item.save()

        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user,
                # user = 'admin@gmail.com',
            )

        return redirect('cart')

    ## If the user is not authenticated
    else:
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]


        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)

            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            item.save()
        else:
            cart_item  = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )

        return redirect('cart')   

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            print(request.user)
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))  #
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass    # simply ignore
    context = {
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
        'cart_items': cart_items,
    }

    return render(request, 'store/cart.html', context)
    # return redirect('cart')    




@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))  #
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass    # simply ignore
    context = {
        'total': total,
        'quantity': quantity,
        'tax': tax,
        'grand_total': grand_total,
        'cart_items': cart_items,
    }
    return render(request, 'store/checkout.html', context)


def remove_cart_item(request, product_id, cart_item_id):

    product = get_object_or_404(Book, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
