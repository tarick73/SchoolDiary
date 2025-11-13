from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect


# Create your views here.

def login_handler(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            nxt = request.GET.get('next') or request.POST.get('next')
            return redirect(nxt or 'profile')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')
def logout_handler(request):
    logout(request)
    return redirect('login')

def register_handler(request):
    if request.method == 'POST':
        username   = request.POST.get('username', '')
        first_name = request.POST.get('firstname', '')
        last_name  = request.POST.get('lastname', '')
        email      = request.POST.get('email', '')
        password   = request.POST.get('password', '')
        user_group = request.POST.get('user_group', '')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name
        )
        if user_group =="teacher":
            user.groups.add(Group.objects.get(name='teacher'))
            user.is_active = False
        else:
            user.groups.add(Group.objects.get(name='student'))

        user.save()

        return redirect('login')

    return render(request, 'register.html')


@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})