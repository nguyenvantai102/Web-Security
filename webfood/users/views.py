from multiprocessing import context
from django.shortcuts import render, redirect

# Create your views here.
from .decorators import admin_only, unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateUserForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .models import Profile


@unauthenticated_user
def loginUser (request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "username or password is incorrect!")
            
    context = {}
    return render(request, 'users/login.html', context)


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid:
            user = form.save()

            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='normal_user')
            user.groups.add(group)

            Profile.objects.create(
				user=user,
				name=user.username,
			)

            messages.success(request, "Dang ky thanh cong!" + username)
            form = CreateUserForm()

            return redirect('login')

    context = {'form':form}
    return render(request, 'users/register.html', context)


@login_required(login_url='login')
def home(request):
    return render(request, 'users/index.html')


@login_required(login_url='login')
def logoutUser (request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
@allowed_users(allowed_roles=['normal_user'])
def user_page (request):
    return render(request, 'users/profile.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['normal_user'])
def account_setting(request):
    _user = request.user.profile
    form = ProfileForm(instance=_user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=_user)
        if form.is_valid():
            form.save()
        

    context = {'form':form}
    return render (request, 'users/account_settings.html', context)


@login_required(login_url='login')
@admin_only
def admin (request):
    return render(request,'users/admin.html')

