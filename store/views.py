from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from category.models import Category
from orders.models import OrderProduct

from carts.models import CartItem
from carts.views import _cart_id
from django.db.models import Q

# # from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# # from .forms import ReviewForm
from django.contrib import messages

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


def search(request):
    products = None
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Book.objects.order_by('-created_date').filter(Q(author__icontains=keyword) | Q(book_title__icontains=keyword))
            product_count = products.count()
        
    context = {
        'products': products,
        # 'product_count': product_count,
    }
    return render(request, 'home.html', context)

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug != None:
        curr_category = get_object_or_404(Category, slug=category_slug)
        products = Book.objects.filter(category=curr_category, is_available=True)
        # paginator = Paginator(products, 3)   #(products, no. of products)
        # page = request.GET.get('page')
        # paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Book.objects.all().filter(is_available=True).order_by('id')
        # paginator = Paginator(products, 3)   #(products, no. of products)
        # page = request.GET.get('page')
        # paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': products,
        # 'products': paged_products,
        # 'product_count': product_count,
    }

    return render(request, 'home.html', context)    