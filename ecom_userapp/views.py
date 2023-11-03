import math
import random
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from ecom_adminapp.models import *
from .models import *
from decimal import Decimal
import random
import string
from django.views.decorators.cache import cache_control
from twilio.rest import Client

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout as django_logout
from django.shortcuts import get_object_or_404
import time
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
def homepage(request):
    produ = Product.objects.all()
    return render(request, 'home.html', {'produ': produ})

def product_detail(request, pk):
    prod = Product.objects.get(id=pk)
    size = ProductSize.objects.filter(product=pk)
    price = Decimal(prod.price)
    offer_price = Decimal(prod.offer_price) if prod.offer_price else Decimal(0)
    discount = int(((price - offer_price) / price) * 100) if price != 0 else 0

    return render(request, 'details.html', {'prod': prod, 'discount': discount, 'size': size})

def cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request, product_id):
    size_name = request.GET.get('size')
    print('haiiiiiiiiiiiiiii')
    print(size_name)
    product = Product.objects.get(pk=product_id)

    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=cart_id(request))
        request.session['has_cart'] = True
        cart.save()

    selected_size = None
    if size_name:
        try:
            product_size = ProductSize.objects.get(product=product, size__name=size_name)
            selected_size = product_size.size
        except ProductSize.DoesNotExist:
            selected_size = None

    

    cart_item = CartItem.objects.filter(product=product, cart=cart, selected_size=selected_size).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        # If no matching cart item exists, create a new one
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
            selected_size=selected_size
        )

    # Redirect to the product detail page
    return redirect('homepage')

def get_cart_item_count(request):
    if request.method == 'GET':
        try:
            cart=Cart.objects.get(cart_id= cart_id(request))
           
            cart_item_count = CartItem.objects.filter(cart=cart,is_active=True).count()
            
            return JsonResponse({'cart_item_count': cart_item_count})
        except Cart.DoesNotExist:
            return JsonResponse({'cart_item_count': 0})
    cart_items = CartItem.objects.filter(cart=cart_id(request))
    total_items_in_cart = cart_items.count()
    context = {
        'cart_items': cart_items,
        'total_items_in_cart': total_items_in_cart,
        
    }
    return render(request, 'home.html', context)



def cart(request):
    total = 0
    quantity = 0
    grand_total = 0
    tax = 0
    cart_items = None
    try:
        if 'phone_number' not in request.session:
            cart = Cart.objects.get(cart_id=cart_id(request))
        else:
            user_login = userloginn.objects.get(mobile_number=request.session.get('phone_number'))
            address_exists = Address.objects.filter(user_login=user_login).exists()
            if address_exists:
                return redirect('checkout_display')
            cart = Cart.objects.get(user_login=user_login)

        cart_items = cart.cartitem_set.filter(is_active=True)
        
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
            cart_item.sub_total = cart_item.product.price * cart_item.quantity
        tax = (2 * total) / 100
        grand_total = round(total + tax)
    except Cart.DoesNotExist:
        pass
    return render(request, 'cart.html', {'total': total, 'quantity': quantity, 'cart_items': cart_items,
                                         'grand_total': grand_total, 'tax': tax})
    
def increase_quantity(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    cart_item.total_price = cart_item.product.offer_price * cart_item.quantity
    return redirect('cart')

def decrease_quantity(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        cart_item.total_price = cart_item.product.offer_price * cart_item.quantity
    return redirect('cart')



def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('cart')




def userlogin(request):
    
 return render(request, 'login.html')




def generate_otp():
    return str(random.randint(1000, 9999))

def send_otp(phone_number, otp):
    client = Client('AC92305620070113393e1445ccdd2ce049', '10cb66e9f34b29e345f541235995a085')
    
    message = client.messages.create(
        body=f'Your OTP is: {otp}',
        from_='+12565677797',
        to=phone_number
    )
    
    
    
def userlogin(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        request.session['temp_phone_number']=phone_number
        # Generate and send OTP
        otp = generate_otp()
        send_otp(phone_number, otp)
        
        # Store OTP in session
        request.session['otp'] = otp
        
        try:
            user = userloginn.objects.get(mobile_number=phone_number)
        except ObjectDoesNotExist:
            
            user = userloginn.objects.create(mobile_number=phone_number)
            
        return redirect('verify_otp')
        
    return render(request, 'login.html')

def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        if entered_otp == stored_otp:
            phone_number = request.session.get('temp_phone_number')
            
            user_login, created =  userloginn.objects.get_or_create(mobile_number=phone_number)
            request.session['phone_number'] = phone_number
            if request.session.get('has_cart'):
                cart=Cart.objects.get(cart_id=cart_id(request))
                if cart is not None:
                    cart.user_login= user_login 
                    cart.save()
            CartItem.objects.filter(cart=request.session.get('cart_id'))
            
            # Clear session data after successful verification
            del request.session['otp']
            # del request.session['phone_number']
            
            context = {'phone_number': phone_number}
            return redirect('cart')
        
        # If OTP validation fails, return an error response
        return HttpResponse("Invalid OTP. Please try again.")
    
    # Render the 'otp.html' template for GET requests
    return render(request, 'otp.html')


def logout(request):
    phone_number = request.session.get('phone_number')
    request.session.clear()
    django_logout(request)
    return redirect('homepage')




def checkout(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        country = request.POST.get('country')
        state = request.POST.get('state')
        district = request.POST.get('district')
        zipcode = request.POST.get('zipcode')
        nearest_land_mark = request.POST.get('nearest_land_mark')
        user_login = userloginn.objects.get(mobile_number=request.session.get('phone_number'))
        address_obj = Address(
            user_login=user_login,
            fullname=fullname,
            address=address,
            country=country,
            state=state,
            district=district,
            zipcode=zipcode,
            nearest_land_mark=nearest_land_mark
        )
        address_obj.save()

        cart = Cart.objects.get(user_login=user_login)
        cart_items = cart.cartitem_set.filter(is_active=True)
        total = 0
        quantity = 0
        grand_total = 0
        tax = 0

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
            cart_item.sub_total = cart_item.product.price * cart_item.quantity
        tax = (2 * total) / 100
        grand_total = round(total + tax)

        address_exists = Address.objects.filter(user_login=user_login).exists()
        if address_exists:
            return redirect('checkout_display')
        else:
            return redirect('address_enter')  # Replace 'address_enter' with your actual URL name for the address entry page

    return render(request, 'checkout.html')

def checkout_display(request):
    user_login = userloginn.objects.get(mobile_number=request.session.get('phone_number'))
    address_objs = Address.objects.filter(user_login=user_login)
    cart = Cart.objects.get(user_login=user_login)
    cart_items = cart.cartitem_set.filter(is_active=True)
    total = 0
    quantity = 0
    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity
        cart_item.sub_total = cart_item.product.price * cart_item.quantity
    tax = (2 * total) / 100
    grand_total = round(total + tax)

    return render(request, 'checkout_display.html', {'address_objs': address_objs, 'total': total, 'quantity': quantity,
                                                    'cart_items': cart_items, 'grand_total': grand_total, 'tax': tax})



def add_to_wishlist(request, product_id):
    user_login = userloginn.objects.get(mobile_number=request.session.get('phone_number'))
    product = Product.objects.get(id=product_id)
    try:
        Wishlist.objects.create(user_login=user_login, product=product)
    except:
        pass
    return redirect('homepage')

def wishlist(request):
    user_login = userloginn.objects.get(mobile_number=request.session.get('phone_number'))
    wishlist_items = Wishlist.objects.filter(user_login=user_login)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
   
   
def delete_wishlist(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id)
    wishlist_item.delete()
    return redirect('wishlist')


def payment(request):
    user_login = userloginn.objects.get(mobile_number=request.session.get('phone_number'))
    address_objs = Address.objects.filter(user_login=user_login)
    cart = Cart.objects.get(user_login=user_login)
    cart_items = cart.cartitem_set.filter(is_active=True)
    total = 0
    quantity = 0
    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += cart_item.product.price * cart_item.quantity
        quantity += cart_item.quantity
        cart_item.sub_total = cart_item.product.price * cart_item.quantity
    tax = (2 * total) / 100
    grand_total = round(total + tax)

    return render(request, 'payment.html', {'address_objs': address_objs, 'total': total, 'quantity': quantity,
                                            'cart_items': cart_items, 'grand_total': grand_total, 'tax': tax})



def stripe_payment(request):
    if request.method == 'POST':
        # Retrieve the necessary details from the request
        
        amount = request.POST.get('amount')  # The amount should be in cents or based on your currency
        order_id = generate_order_id()  # Call the function to generate an order ID

        # Create a charge
        try:
            # Stripe configuration with your secret key
           


            # Save payment data to the model
            user_login = userloginn.objects.get(mobile_number=request.session.get('phone_number'))
            payment = Payments(
                user_login=user_login,  # Adjust based on your user authentication logic
                order=None,  # Modify based on your implementation, allow null and blank values
                selected_size=None,  # Adjust based on your requirement
                payment_method='Stripe',  # Assuming payment method is Stripe
                amount_paid=amount,
                order_number=order_id
            )
            payment.save()

            # Set cart items to inactive here
            cart = Cart.objects.get(cart_id=cart_id(request))
            cart.is_active = False
            cart.save()
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            # Mark the cart items as purchased or set is_active to False
            for cart_item in cart_items:
                cart_item.is_active = False  # Set is_active to False to indicate item is purchased
                cart_item.save()
            stripe.api_key = "sk_test_51O8H0eSBStAe3jnhci3V6qVZaLEEjA36GOZMag7RkHUse3NL4Tmbk42LKlxb7CIr4I8rj6QIhw63nLo0h8CdUg7400XT9uRaiZ"
            
            charge = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            payment_method_types=['card'],
        )
            user_login = userloginn.objects.get(mobile_number=request.session.get('phone_number'))
            send_payment_received_message(user_login.mobile_number)
            return redirect('success')

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            print(f"Status is: {e.http_status}")
            print(f"Type is: {err.get('type')}")
            print(f"Code is: {err.get('code')}")
            print(f"Param is: {err.get('param')}")
            print(f"Message is: {err.get('message')}")
            return render(request, 'error.html')
    
    return render(request, 'payment.html')

def generate_order_id():
    # Implement your logic to generate an order ID here
    # You can use datetime or a unique identifier
    
    order_id = f"ORDER_{int(time.time())}"
    return order_id



def success(request):
    
    user_login = userloginn.objects.get(mobile_number=request.session.get('phone_number'))
    address_objs = Address.objects.filter(user_login=user_login)
    
    total = 0
    quantity = 0
    grand_total = 0
    tax = 0
    cart_items=None
    try:
        cart = Cart.objects.get(cart_id=cart_id(request))
        cart_items = CartItem.objects.filter(cart_id=cart).order_by('-is_active')
        

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        # cart_item.sub_total = cart_item.product.price * cart_item.quantity
        tax = (2 * total) / 100
        grand_total = round(total + tax)
    except ObjectDoesNotExist:
        pass

    return render(request, 'success.html', {'address_objs': address_objs, 'total': total, 'quantity': quantity,
                                                    'cart_items': cart_items, 'grand_total': grand_total, 'tax': tax})


def send_payment_received_message(mobile_number):
    client = Client('AC92305620070113393e1445ccdd2ce049', '10cb66e9f34b29e345f541235995a085')  # Replace with your Twilio credentials
    message = client.messages.create(
        body="Your payment has been received. Thank you for shopping with us!",
        from_='+12565677797',
        to=mobile_number
    )