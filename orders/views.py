from django.shortcuts import render,redirect
from django.http import JsonResponse
from carts.models import CartItem
# from .forms import OrderForm
from .models import Order, Payment, OrderProduct
from store.models import Book
import datetime
import json

# Create your views here.
def place_order(request):
    return render(request, 'orders/payments.html')


def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])


    # Store transaction details inside Payment Model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],

    )
    payment.save()

    order.payment = payment         ## 'foreign key' field
    order.is_ordered = True
    order.save()

    # Move the cart items to OrderProduct table
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

    # Reduce the quantity of the sold Products
    product = Product.objects.get(id=item.product_id)
    product.stock -= item.quantity
    product.save()


    # Clear cart
    CartItem.objects.filter(user=request.user).delete()

    # Send order received email to customer

    # Send order number and transaction id back to sendData method via json response
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }

    return JsonResponse(data)



def order_complete(request):

    # order_number = request.GET.get('order_number')
    # transID = request.GET.get('payment_id')
    # try:
    #     order = Order.objects.get(order_number=order_number, is_ordered=True)
    #     ordered_products = OrderProduct.objects.filter(order_id=order.id)

    #     subtotal = 0
    #     for i in ordered_products:
    #         subtotal += i.product_price * i.quantity

    #     payment = Payment.objects.get(payment_id=transID)
    #     context = {
    #         'order': order,
    #         'ordered_products': ordered_products,
    #         'order_number': order.order_number,
    #         'transID': payment.payment_id,
    #         'payment': payment,
    #         'subtotal': subtotal,
    #     }

    #     return render(request, 'orders/order_complete.html', context)

    # except (Payment.DoesNotExist, Order.DoesNotExist):
    #     return redirect('home')


    return render(request, 'orders/order_complete.html')

