from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterUser
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.core.mail import send_mail
from django.conf import settings
from tasks.models import Plan, Task
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required

# Create your views here.

# This code sends reminders of tasks as emails
while True:
    tasks = Task.objects.filter(date_created__gte = (datetime.now().date() - timedelta(days=1)))
    for task in tasks:
        if (task.start_date - datetime.today().date()).days <= 1 and task.reminder == False:
            send_mail(f'Reminder for {task.title}',
                    f'''You are reminded that your task,
                    "{task.title}" is starting tomorrow at 
                    {task.start_time}.\n
                    Click on this link to get redirected.\n
                    👇👇👇👇👇👇\n
                    http://planhub.pythonanywhere.com/tasks/task/{task.id}''',
                    'settings.EMAIL_HOST_USER',
                    [task.plan.user.email],
                    False,)
            task.reminder = True
            task.save()
    break
# Code for emails ends here

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home/home.html')



def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Wrong Credentials!')
            return render(request, 'home/login.html')
        
    else:
        return render(request, 'home/login.html')


def logoutUser(request):
    messages.success(request, 'Successfully logged out')
    logout(request)
    return redirect('login')


def sign_up(request):
    form = RegisterUser()
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)          
            messages.success(request, 'Account created successfully')
            return redirect('dashboard')

    return render(request, 'home/sign_up.html', {'form':form})


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Check if the email exists in your User model
        # If the email exists, generate a random code and store it in your database
        # You can use the `random` module to generate a random code
        # Then, send the code to the user's email using a third-party email service or built-in Django email functionality
        # Finally, redirect the user to a new page where they can enter the code
        
        # For now, we'll just display a message to the user to check their email
        messages.success(request, 'A code has been sent to your email. Please check your inbox.')
        
    return render(request, 'home/forgot_password.html')

@login_required
def profile(request):
   return render(request, "home/profile.html")

@login_required
def update_profile(request):
    user = request.user

    # Handle profile details update
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        user.save()
        messages.success(request, 'Your profile details have been updated.')
        # Redirect back to the profile page
        return redirect('profile')

    return render(request, 'home/update_profile.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Updating the session with the new password
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'home/change_password.html', {'form': form})