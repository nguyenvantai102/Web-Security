from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponseRedirect, HttpResponse
from food_diet.models import Blog, Diet

from .decorators import admin_only, unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateUserForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from .models import Profile
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User

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
    return render(request, 'users/templates/users/login.html', context)


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)

            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='normal_user')
            user.groups.add(group)

            Profile.objects.create(
				user=user,
				name=user.username,
			)
            mail_subject = 'Activate your account.'
            message = render_to_string('active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            return HttpResponse('Tạo tài khoản thành công, vui lòng kiểm tra email để kích hoạt tài khoản')
    context = {'form':form}
    return render(request, 'users/templates/users/register.html', context)

# Activate registration
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
        #return HttpResponse('Cảm ơn bạn đã xác nhận email. Tài khoản của bạn đã được kích hoạt')
    else:
        return HttpResponse('Liên kết kích hoạt tài khoản không hợp lệ!')

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
    return render(request, 'users/templates/users/profile.html')


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
    return render (request, 'users/templates/users/account_settings.html', context)


@login_required(login_url='login')
@admin_only
def admin (request):
    return render(request,'users/templates/users/admin.html')


# Chức năng đề xuất
result = {}
def get_info(request):
    global result
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        gender = request.POST['gender']
        gender = gender.lower()
        age = int(request.POST['age'])
        high = int(request.POST['high']) 
        weight = int(request.POST['weight'])
        
        if gender == 'nam':
            # Tính BMR cho nam
            BMR = 66.5 + (13.75 * weight) + (5.003 * high) - (6.755 * age)
        else:
            # Tính BMR cho nữ
            BMR = 55.1 + (9.563 * weight) + (1.850 * high) - (4.676 * age)

        # Tính Calo trung bình
        calo = BMR * 1.5

        type = 0
        if calo < 800:
            type = 1
        elif calo > 800 and calo <= 1100:
            type = 2
        elif calo > 1100 and calo <= 1400:
            type = 3
        elif calo > 1400 and calo <= 1700:
            type = 4
        elif calo > 1700 and calo <= 2000:
            type = 5
        elif calo > 2000 and calo <= 2300:
            type = 6
        elif calo > 2300 and calo <= 2600:
            type = 7
        else:
            type = 8

        high = high / 100
        BMI = weight / (2 * high)
        
        search = ""
        if BMI < 18.5:
            search = "weight_gain"
        elif BMI >= 25:
            search = "loss_gain"
        else:
            search = "other"

        result["search"] = search
        result["type"] = type

        return HttpResponseRedirect('/propose')

    return render(request, 'users/templates/menu/service.html')

def propose(request):
    blog = Blog.objects.filter(topic__contains=result["search"]).all()
    diet = Diet.objects.filter(type=result["type"]).all()
    return render(request, 'users/templates/menu/blog.html', {"blog": blog, "diet": diet})






@login_required(login_url='login')
#About
def about_view(request):
    return render(request, 'users/templates/menu/about.html')


@login_required(login_url='login')
# Service
def service_view(request):
    return render(request, 'users/templates/menu/service.html')