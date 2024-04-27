from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from category.models import Category
from orders.models import OrderProduct

# from carts.models import CartItem
# from carts.views import _cart_id
# from django.db.models import Q

# # from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# # from .forms import ReviewForm
# from django.contrib import messages

# Create your views here.
def product_detail(request, category_slug, product_slug):
    try:
        single_product = Book.objects.get(category__slug=category_slug, slug=product_slug)
        # in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    # # try:
    # #     orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
    # # except OrderProduct.DoesNotExist:
    # #     orderproduct = None

    context = {
    'single_product': single_product,
    # 'in_cart'       : in_cart,
    # 'orderproduct'  : orderproduct,
    }

    return render(request, 'store/product_detail.html', context)