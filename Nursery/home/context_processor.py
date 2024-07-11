from .views import *
from cart.views import *
from cart.views import *


def categ(request):

    c_plant=categ_plants.objects.all()
    plant_obj = add_plants.objects.all().annotate(posts_count=Count('slug'))

    return {'cp':c_plant,'po':plant_obj}

def cart_total(request):
    total=0
    count=0
    disc=0
    grand_total=0
    shpg_charge=50

    user = request.user
    if user.is_authenticated:
        ct=cartlist.objects.filter(user=user)
    else:
        cart_id=request.session.get('cart_id')
        ct=cartlist.objects.filter(cart_id=cart_id)

    ct_items=items.objects.filter(cart__in=ct,active=True)
    for i in ct_items:
        total += (i.plant_obj.price * i.quantity)
        count += i.quantity
        disc = total * (10 / 100)
        grand_total = total - disc+shpg_charge
    return {'ci':ct_items,'t':total,'cn':count,'dsc':disc,'gt':grand_total,'sc':shpg_charge}

# def nersery_profile_context(request):
#     admin_id = request.GET.get('admin_id')
#     plantAdmin = get_object_or_404(plant_admin, id=admin_id)
#     return {'N_Admin': plantAdmin}
