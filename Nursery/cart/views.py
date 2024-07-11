from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import *
from home.models import *
from account.models import *

# Create your views here.
def cart_detaials(request,total=0,count=0,disc=0,grand_total=0,shpg_charge=50):
    try:
        user=request.user
        if user.is_authenticated:
            ct=cartlist.objects.filter(user=user)

        else:
            cart_id=request.session.get('cart_id')
            ct=cartlist.objects.filter(cart_id=cart_id)
        ct_items = items.objects.filter(cart__in=ct, active=True)
        for i in ct_items:
            total += (i.plant_obj.price * i.quantity)
            count += i.quantity
            disc = total * (10 / 100)
            grand_total = total - disc+shpg_charge
    except ObjectDoesNotExist:
        return HttpResponse("<script> alert('Empty Cart');window.location='/';</script>")
    return render(request,'cart.html',{'ci':ct_items,'t':total,'cn':count,'dsc':disc,'gt':grand_total,'sc':shpg_charge})
def c_id(request):
    cart_id=request.session.session_key
    if not cart_id:
        cart_id=request.session.create()
    return cart_id
@login_required(login_url='user_login')
def add_cart(request,plant_id):
    plant_obj=add_plants.objects.get(id=plant_id)
    user=request.user

    try:
        ct=cartlist.objects.get(user=user)
    except cartlist.DoesNotExist:
        ct=cartlist.objects.create(cart_id=c_id(request),user=user)
        ct.save()

    try:
        c_items=items.objects.get(plant_obj=plant_obj,cart=ct)
        if c_items.quantity < c_items.plant_obj.stock:
            c_items.quantity +=1
            plant_obj.stock -=1
            plant_obj.save()
        c_items.save()
    except items.DoesNotExist:
        c_items=items.objects.create(plant_obj=plant_obj,quantity=1,cart=ct)
        plant_obj.stock -=1
        plant_obj.save()
        c_items.save()
    return redirect('cart_details')



@login_required(login_url='user_login')
def decrement_cart(request,plant_id):
    user=request.user
    try:
        if user.is_authenticated:
            ct_list=cartlist.objects.filter(user=user)
        else:
            cart_id=request.session.get('cart_id')
            ct_list=cartlist.objects.filter(cart_id=cart_id)
        if ct_list.exists:
            for ct in ct_list:
                plant_obj=get_object_or_404(add_plants,id=plant_id)
                try:
                    c_items=items.objects.get(plant_obj=plant_obj,cart=ct)
                    if c_items.quantity>1:
                        c_items.quantity-=1
                        c_items.save()
                    else:
                        c_items.delete()
                except items.DoesNotExist:
                    pass
    except cartlist.DoesNotExist:
        pass
    return redirect('cart_details')
@login_required(login_url='user_login')
def remove_cart(request,plant_id):
    user=request.user
    try:
        if user.is_authenticated:
            ct_list=cartlist.objects.filter(user=user)
        else:
            cart_id=request.session.get('cart_id')
            ct_list=cartlist.objects.filter(cart_id=cart_id)
        if ct_list.exists:
            for ct in ct_list:
                plant_obj=get_object_or_404(add_plants,id=plant_id)
                try:
                    c_items=items.objects.get(plant_obj=plant_obj,cart=ct)

                    c_items.delete()
                except items.DoesNotExist:
                    pass
    except cartlist.DoesNotExist:
        pass
    return redirect('cart_details')

def checkout(request):
    if request.method== 'POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        phone=request.POST['phone']
        address=request.POST['address']
        state=request.POST['state']
        towncity=request.POST['city']
        country=request.POST['country']
        postcodezip=request.POST['postcode']
        cart=cartlist.objects.filter(user=request.user).first()
        check_out=Checkout(
            user=request.user,
            cart=cart,
            firstname=firstname,
            lastname=lastname,
            country=country,
            state=state,
            address=address,
            towncity=towncity,
            postcodezip=postcodezip,
            phone=phone,
            email=email)
        check_out.save()
        return redirect('payment')

    return render(request,'checkout.html')
def payments(request):
    if request.method=='POST':
        account_number=request.POST.get('account_number')
        name=request.POST.get('name')
        expiry_month=request.POST.get('expiry_month')
        expiry_year=request.POST.get('expiry_rear')
        cvv=request.POST.get('cvv')

        pay=payment(
            user=request.user,
            account_number=account_number,
            name=name,
            expiry_month=expiry_month,
            expiry_year=expiry_year,
            cvv=cvv

        )
        pay.save()
        return redirect('success')
    return render(request,'payment.html')




def success(request):
    latest_checkout = Checkout.objects.latest('id')
    # Redirect to generate_bill view with the checkout_id
    return redirect('generate_bill', checkout_id=latest_checkout.id)
    return render(request,'success.html')


@login_required(login_url='user_login')
def generate_bill(request, checkout_id):
    checkout_info = get_object_or_404(Checkout, id=checkout_id, user=request.user)
    payment_info = payment.objects.filter(user=request.user).last()

    try:
        cart = checkout_info.cart
        order_items = items.objects.filter(cart=cart)
        order_items_with_plants = [{'item': item, 'plant': get_object_or_404(add_plants, id=item.plant_obj.id)} for item
                                   in order_items]

        # Creating an OrderManagement object for each order item
        for order_item_data in order_items_with_plants:
            order_item = order_item_data['item']
            plant = order_item_data['plant']
            OrderManagement.objects.create(
                customer_checkout=checkout_info,
                order_item=order_item,
                plant=plant
            )

        # Clear the cart items after storing them in OrderManagement
        order_items.delete()

    except items.DoesNotExist:
        order_items_with_plants = []

    total = sum(item['plant'].price * item['item'].quantity for item in order_items_with_plants)
    discount = total * 0.10  # 10% discount
    shipping_charge = 50  # Example: $50
    grand_total = total - discount + shipping_charge

    return render(request, 'bill_template.html', {
        'checkout': checkout_info,
        'payment_info': payment_info,
        'order_items': order_items_with_plants,
        'Total': total,
        'discount': discount,
        'shipping_charge': shipping_charge,
        'grand_total': grand_total,
    })



def manage_checkouts(request, admin_id):
    nursery_admin = get_object_or_404(plant_admin, id=admin_id)

    admin_plants = add_plants.objects.filter(admin=nursery_admin)

    checkouts = Checkout.objects.filter(cart__items__plant_obj__in=admin_plants)

    checkout_items = []
    for checkout in checkouts:
        order_items = OrderManagement.objects.filter(customer_checkout=checkout)
        item_details = []
        for order_item in order_items:
            item = order_item.order_item
            item_detail = {
                'plant': item.plant_obj,
                'quantity': item.quantity
            }
            item_details.append(item_detail)
        checkout_data = {
            'checkout': checkout,
            'order_items': item_details
        }
        checkout_items.append(checkout_data)

    return render(request, 'manage_checkouts.html', {'N_Admin': nursery_admin, 'checkout_items': checkout_items})




