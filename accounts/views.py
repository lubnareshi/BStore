from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required


# Verification EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.views import _cart_id
from carts.models import Cart, CartItem
import requests

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.is_admin = True
            user.is_active = True
            user.is_staff = True
            user.save()

            # USER ACTIVATION
            # current_site = get_current_site(request)
            # mail_subject = 'Please activate your account'
            # message = render_to_string('accounts/account_verification_email.html', {
            #     'user': user,
            #     'domain': current_site,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user),
            # })

            # to_email = email
            # send_email = EmailMessage(mail_subject, message, to=[to_email])
            # send_email.send()


            messages.success(request, 'Registration Successful.')
            return redirect('register')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # print(email)
        # print(password)

        user = auth.authenticate(email=email, password=password)
        


        if user is not None:   ## Means User Present
            # try:        ## prior login things
            #     # cart = Cart.objects.get(cart_id=_cart_id(request))
            #     # is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
            #     # if is_cart_item_exists:
            #     #     cart_item = CartItem.objects.filter(cart=cart)     # vl give all current cart items


            # except:
            #     pass

            auth.login(request, user)       ## login
            # messages.success(request, "You are now logged in.")
            return redirect('home')
            # url = request.META.get('HTTP_REFERER')
            # try:
            #     query = requests.utils.urlparse(url).query
            #     # next=/cart/checkout
            #     params = dict(x.split('=') for x in query.split('&'))
            #     if 'next' in params:
            #         nextPage = params['next']
            #         return redirect(nextPage)

            # except:
            #     return redirect('dashboard')
        else:                   ## User Absent
            messages.error(request, 'Invalid Login Credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')



# def activate(request):
#     return


def dashboard(request):
    return render(request, 'accounts/dashboard.html')



def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            ## Send email code Goes here

        else:
            messages.error(request, 'Account Does Not Exist')
    return render(request, 'accounts/forgotPassword.html')
