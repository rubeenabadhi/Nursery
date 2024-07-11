from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.shortcuts import render, redirect, get_object_or_404,reverse

from .models import *


# Create your views here.



def register(request):
    if request.method=="POST":
        first_name= request.POST["first_name"]
        last_name= request.POST["last_name"]
        username= request.POST["username"]
        password1= request.POST["password1"]
        password2= request.POST["password2"]
        email= request.POST["email"]

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username is already taken')
                return redirect("register")
            elif User.objects.filter(email=email).exists():
                messages.error(request,"email is already taken")
                return redirect("register")

            else:
                user= User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()

        else:
            messages.info(request, "passwords are not equel")
            return redirect("register")
        return redirect("/")
    else:
        return render(request,"signup.html")

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password= request.POST['password']
        user= auth.authenticate(username=username,password=password)
        print(user)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid details')
            return redirect('user_login')
    else:
        return render(request,'login.html')



def logout(request):
    auth.logout(request)
    return redirect('/')



def nursery_signup(request):
    if request.method == "POST":
        name = request.POST["name"]
        mob_num = request.POST["mob_num"]
        photo = request.FILES.get('photo')
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        email = request.POST["email"]
        nursery_address = request.POST['address']

        if password1 == password2:
            if plant_admin.objects.filter(name=name).exists():
                messages.info(request, 'Name is already taken')
                return redirect("nursery_signup")
            elif plant_admin.objects.filter(email=email).exists():
                messages.info(request, "Email is already taken")
                return redirect("nursery_signup")
            elif plant_admin.objects.filter(mob_num=mob_num).exists():
                messages.info(request, "Mobile number is already taken")
                return redirect("nursery_signup")
            elif plant_admin.objects.filter(nursery_address=nursery_address).exists():
                messages.info(request, "Nursery address is already taken")
                return redirect("nursery_signup")
            else:
                nursery_admin = plant_admin.objects.create(
                    name=name, photo=photo, password1=password2, email=email, mob_num=mob_num, nursery_address=nursery_address
                )
                nursery_admin.save()
                messages.success(request, 'Nursery admin registered successfully!')
                return redirect('nursery_login')
        else:
            messages.error(request, "Passwords are not equal")
            return redirect("nursery_signup")

    else:
        return render(request, "pladmin_signup.html")

    nsry_admin = plant_admin.objects.all()
    return render(request, "pladmin_signup.html", {'na': nsry_admin})


def nersery_profile(request,admin_id):
    plantAdmin = get_object_or_404(plant_admin, id=admin_id)
    print(plantAdmin, 'admin')

    return render(request,'nursery_profile.html',{'N_Admin':plantAdmin})


def nursery_login(request):
    if request.method == 'POST':
        mob_num = request.POST['mob_num']
        password = request.POST['password']

        try:
            nursery_admin = plant_admin.objects.get(mob_num=mob_num, password1=password, approve=True)
            return redirect('nersery_profile', admin_id=nursery_admin.id)
        except plant_admin.DoesNotExist:
            messages.info(request, 'Invalid details')


    return render(request,'pladmin_login.html' )

def admin_logout(request):
    logout(request)
    return redirect('/')

# Update it here
@login_required
def useredit_profile(request):
    if request.method == 'POST':
        fn=request.POST['first_name']
        ln=request.POST['last_name']
        usernm=request.POST['username']
        email=request.POST['email']

        if User.objects.filter(username=usernm).exists():
            messages.info(request,'username is already taken')
            return redirect("edit_profile")
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'email is already taken')
            return redirect("edit_profile")
        else:
            usr=User.objects.get(id=request.user.id)
            usr.first_name=fn
            usr.last_name=ln
            usr.username=usernm
            usr.email=email
            usr.save()
            return redirect('dashboard')

    return render(request, 'useredit_profile.html')


@login_required(login_url='user_login')  # Ensure the user is logged in to access this view
def delete_account(request):
    if request.method == 'POST':
        # Delete the user account
        user = request.user
        user.delete()
        return redirect('home')  # Redirect to the home page or any other desired page after deletion

    return render(request, 'delete_account.html')  # Display a confirmation page with a form to delete the account

def nursery_editprofile(request, admin_id):
    plantAdmin = get_object_or_404(plant_admin, id=admin_id)

    if request.method == 'POST':
        NurseryName=request.POST['name']
        email=request.POST['email']
        adrs=request.POST['address']
        mobile=request.POST['mobile']
        img = request.FILES.get('photo')
        oldpaswd=request.POST['oldpswd']
        paswd1=request.POST['newpaswd1']
        paswd2=request.POST['newpaswd2']
        if oldpaswd == plantAdmin.password1:
            if paswd1==paswd2:

                if plant_admin.objects.filter(name=NurseryName).exclude(id=admin_id).exists():
                    messages.error(request, 'Username is already taken')
                    return redirect('nursery_editprofile', admin_id=admin_id)
                elif plant_admin.objects.filter(email=email).exclude(id=admin_id).exists():
                    messages.error(request, 'Email is already taken')
                    return redirect('nursery_editprofile', admin_id=admin_id)
                elif plant_admin.objects.filter(mob_num=mobile).exclude(id=admin_id).exists():
                    messages.error(request, 'Mobile is already taken')
                    return redirect('nursery_editprofile', admin_id=admin_id)

                else:
                    plantAdmin.name = NurseryName
                    plantAdmin.email = email
                    plantAdmin.mob_num = mobile
                    plantAdmin.nursery_address = adrs
                    if img:
                        plantAdmin.photo = img
                    plantAdmin.photo = img
                    plantAdmin.password1 = paswd1
                    plantAdmin.save()
                    messages.success(request, 'Your Profile Successfully Updated')
                    return redirect('nersery_profile', admin_id=admin_id)

            else:
                messages.error(request, 'Old password is not valid')
                return redirect('nursery_editprofile', admin_id=admin_id)

    return render(request,'nursery_editprofile.html', {'N_Admin':plantAdmin})




def forgotPassword(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if password1 == password2:
                user.set_password(password1)
                user.save()
                messages.success(request, 'Password reset successful')
                return redirect('user_login')
            else:
                messages.error(request, 'Passwords do not match.')
        elif plant_admin.objects.filter(name=username).exists():
            user = plant_admin.objects.get(name=username)
            if password1 == password2:
                user.password1 = password1
                user.password2 = password2
                user.save()
                messages.success(request, 'Password reset successful..')
                return redirect('nursery_login')
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'Username is not valid.')

    return render(request, 'forgot_password.html')






