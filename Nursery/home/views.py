from django.contrib import messages

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,InvalidPage

from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import add_plants, categ_plants, Feedback, Contact
from account.models import *

# Create your views here.

def addplant_item(request, admin_id):
    plantAdmin = get_object_or_404(plant_admin, id=admin_id)

    if request.method == 'POST':
        admin = plantAdmin  # Corrected variable name
        name = request.POST['name']
        photo = request.FILES.get('photo')
        category = request.POST['category']
        price = request.POST['price']
        details = request.POST['details']
        stock = request.POST['stock']
        category_obj = categ_plants.objects.get(name=category)
        plants = add_plants.objects.create(admin=admin, name=name, img=photo, category=category_obj, price=price, details=details, stock=stock)
        plants.save()
        messages.success(request, 'Successfully Added')
        return redirect('addplant_item', admin_id=admin_id)

    return render(request, 'plants_form.html', {'N_Admin': plantAdmin, 'Admin_id': admin_id})

def nursery_dashboard(request):
    return render(request,"nurserydashboard.html")


def home(request,cat_slug=None):
    if cat_slug != None:
        catg_obj=get_object_or_404(categ_plants,slug=cat_slug)
        plant_obj =add_plants.objects.filter(category=catg_obj,available=True)
    else:
        plant_obj = add_plants.objects.all().filter(available=True)

    c_plant=categ_plants.objects.all()
    c_feedback=Feedback.objects.all()

    # --------Paginator
    p = Paginator(plant_obj, 4)

    pageNum = int(request.GET.get('page', 1))

    try:
        proe = p.page(pageNum)
        print(proe)
    except(EmptyPage, InvalidPage):
        proe = p.page(p.num_pages)
        # -------------End paginator

    return render(request,'home_index.html',{'cp':c_plant,'po':plant_obj,'pr':proe,'feedback':c_feedback})

def searching(request,):
    if 'q' in request.GET:
        query=request.GET.get('q')
        plant_obj=add_plants.objects.all().filter(Q(name__icontains=query)|Q(details__icontains=query),available=True)
    if not plant_obj:
        return HttpResponse('<h1>not available</h1>')

    return render(request,'search.html',{'pl':plant_obj})


def plant_details(request,cat_slug,plant_slug):
    plant_obj=add_plants.objects.get(category__slug=cat_slug,slug=plant_slug)

    return render(request,'shop-details.html',{'po':plant_obj})

def about(request):
    return render(request,'about.html')

def shop(request):
    c_plant=categ_plants.objects.all()
    plant_obj = add_plants.objects.all().annotate(posts_count=Count('slug'))

    for i in plant_obj:
        print(i.posts_count)

    return render(request,'shop.html',{'cp':c_plant,'po':plant_obj})

def blog(request):

    return render(request,'blog.html')
def user_dashboard(request):

    return render(request,'user_dashboard.html')

#------------------Send feedback for customer------------------------
def send_feedback_view(request):
    if request.method == 'POST':
        name=request.POST['name']
        plant=request.POST['Plant']
        feedback=request.POST['feedback']
        plant_item=add_plants.objects.get(name=plant)
        print(plant_item)

        cus_feedback=Feedback.objects.create(plant=plant_item,name=name,feedback=feedback)
        cus_feedback.save()
        return redirect('feedback_done')

    return render(request, 'send_feedback.html')
def feedback_done(request):
    return render(request,'feedback_done.html')

def view_feedback(request,admin_id):
    nursery_admin = get_object_or_404(plant_admin, id=admin_id)
    Plants =nursery_admin.N_Plants.all()  # N_Plants=related name is 'add_plants' admin
    feedback= Feedback.objects.filter(plant__in=Plants)
    return render(request,'feedbackView.html',{'feedback':feedback,'N_Admin':nursery_admin})


def admin_plants(request, admin_id):
    nursery_admin = get_object_or_404(plant_admin, id=admin_id)

    admin_plants = add_plants.objects.filter(admin__id=admin_id)

    return render(request, 'admin_plants.html', {'admin_plants': admin_plants,'N_Admin':nursery_admin})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Validate the form data as needed

        Contact.objects.create(name=name, email=email, subject=subject, message=message)
        return redirect('contact')  # Redirect to a success page after successful form submission

    return render(request, 'contact.html')




from django.shortcuts import get_object_or_404

def edit_plant(request, plant_id):
    # Retrieve the plant item to be edited based on its ID
    plant = get_object_or_404(add_plants, id=plant_id)

    if request.method == 'POST':
        # Get the data from the request
        name = request.POST['name']
        photo = request.FILES.get('photo')
        price = request.POST['price']
        details = request.POST['details']
        stock = request.POST['stock']

        # Update the plant item with the new data
        plant.name = name
        if photo:
            plant.img = photo
        plant.price = price
        plant.details = details
        plant.stock = stock
        plant.save()

        return redirect('admin_plants', admin_id=plant.admin.id)  # Redirect to admin plants page after successful update

    return render(request, 'edit_plants.html', {'plant': plant})

