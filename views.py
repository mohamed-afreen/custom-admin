from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


# from django.db.models import Search
from django.contrib import messages



# Create your views here.

def admin_dashboard(request):

    if 'search' in request.GET:
        search = request.GET['search']
        user_list = User.objects.filter(first_name__icontains=search)
        # multiple_search = Search(Search(first_name__icontains=search) | Search(last_name__icontains=search))
        # user_list = User.objects.filter(multiple_search)

    else:
        user_list = User.objects.all()

    context = {
        "user_list":user_list
    }
    return render(request,'dashboard.html',context)

    # if 'username' in request.session:        ---(we can write this like also)--
    #     return render(request,'dashboard.html',{"user_list":user_list})
    # return redirect(admin_panel)


def admin_panel(request):

    if 'username' in request.session:
        return redirect(admin_dashboard)

   
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username, password=password)

        if user is not None and user.is_superuser:
                request.session['username'] = username
                return redirect(admin_dashboard)

        else:
            messages.info(request,'invalid credentials')
            return redirect(admin_panel)
    else:
        return render(request, 'admin_login.html')


def add_user(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username already taken')
                return redirect(add_user)

            elif User.objects.filter(email=email).exists():
                messages.info(request,'email is already taken')
                return redirect(add_user)
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password2)
                user.save();
                print('user created')
                return redirect(admin_dashboard)

        else:
            messages.info(request,'password not matching')
            return redirect(add_user)
    return render(request,'add_user.html')


def edit_user(request, user_id):
    edited_user = User.objects.get(pk=user_id)

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']

        edited_user.first_name = first_name
        edited_user.last_name = last_name
        edited_user.username = username
        edited_user.email = email

        edited_user.save()
        return redirect(admin_dashboard)

    return render(request, "edit_user.html",  {"user_list":edited_user})
        


def delete_user(request, user_id):
       del_list = User.objects.get(pk=user_id)
       del_list.delete()
       return redirect(admin_dashboard)


def admin_logout(request):
    
    if 'username' in request.session:
        request.session.flush()
    return redirect(admin_panel)