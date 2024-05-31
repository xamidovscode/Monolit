from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
import bcrypt


def index(request):
    users = User.objects.all().order_by('-id')
    return render(request, 'login_register_app/index.html', {'users': users})


def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.add_message(request, messages.ERROR, value, extra_tags='register')
            return redirect('/')
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
            request.session['user_id'] = user.id
            return redirect("/success")
    else:
        return redirect("/")


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                request.session['user_id'] = user.id
                return redirect("/wall")
            else:
                messages.error(request, "Invalid email or password", extra_tags='login')
                return redirect('/')
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password", extra_tags='login')
            return redirect('/')
    return redirect('/')


def wall(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            "user": User.objects.get(id=request.session['user_id'])
        }
        return render(request,'login_register_app/dash.html', context)


def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            "user": User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'login_register_app/success.html', context)


def reset(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        request.session.clear()
        print("session has been cleared")
        return redirect("/")

