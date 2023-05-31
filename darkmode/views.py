from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from tasks.forms import TaskForm
from tasks.models import Plan
from tasks.models import Task
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tasks.forms import TaskForm,PlanForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, update_session_auth_hash
# import datetime
from tasks.models import Plan
# from tasks import views

# Create your views here.

@login_required(login_url='login')
def dark_index(request):
    user_id = request.user.id
    user_plans = Plan.objects.filter(user__id=user_id)
    tasks = []
    for plan in user_plans:
        plan_tasks = Task.objects.filter(plan__id=plan.id)
        for task in plan_tasks:
            if (datetime.datetime.today().date() - task.end_date).days > 7:
                task.delete()
            tasks.append(task)
        
    count_of_tasks = 0
    sorted_tasks = sorted(tasks, key=lambda x: x.end_date)
    deadline_tasks = []
    for task in sorted_tasks:
        if count_of_tasks < 4:
            deadline_tasks.append(task)
            count_of_tasks = count_of_tasks + 1
        
    return render(request,'darkmode/darkboard.html',
                  {'user_plans':user_plans,
                   'tasks':tasks,
                   'deadline_tasks':deadline_tasks})

@login_required
def create_task(request,pk):
    plans = Plan.objects.filter(user = request.user)
    parent_plan = Plan.objects.get(id=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        print('data submitted ')
        print(form)
        if form.is_valid():
            print('data validated ')
            task = form.save(commit=False)
            print('commit saved ')
            task.user = request.user
            task.save()
            messages.success(request, 'Task added successfully!')
            return redirect('task_list2')
        else:
            messages.error(request, 'Error adding task. Please check the form.')
            return redirect('create-task2')
    else:
        form = TaskForm()

        context = {'form': form, 'parent_plan':parent_plan, 'plans':plans}
        return render(request, 'darkmode/add_task.html', context)

@login_required
def create_new_task(request):
    plans = Plan.objects.filter(user = request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        print('data submitted ')
        print(form)
        if form.is_valid():
            print('data validated ')
            task = form.save(commit=False)
            print('commit saved ')
            task.user = request.user
            task.save()
            messages.success(request, 'Task added successfully!')
            return redirect('task_list2')
        else:
            messages.error(request, 'Error adding task. Please check the form.')
            return redirect('create-task2')
    else:
        form = TaskForm()

        context = {'form': form, 'plans':plans}
        return render(request, 'darkmode/add_task.html', context)

def createPlan(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            return redirect('darkboard')
        else:
            messages.error(request, 'Error adding plan')
            print(form.errors)
    else:
        form = PlanForm()
    return render(request, 'darkmode/add_plan.html', {'form': form})

def task_view(request, pk):
    # task = get_object_or_404(Task, id=task_id)
    task = Task.objects.get(id=pk)
    context = {'task': task}
    return render(request, 'darkmode/task_view.html', context)    



def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task.save()
            return redirect('task_view2', pk)
    return render(request, 'darkmode/update_task.html', {'form':form})

def updatePlan(request, pk):
    plan = Plan.objects.get(id=pk)
    form = PlanForm(instance=plan)
    if request.method == 'POST':
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            plan.save()
            return redirect('darkboard')
    return render(request, 'darkmode/update_plan.html', {'form':form})

def deleteViewTask(request, pk):
    task = Task.objects.get(id=pk)
    return render(request, 'darkmode/delete_task.html', {'task':task})

def deleteViewPlan(request, pk):
    plan = Plan.objects.get(id=pk)
    return render(request, 'darkmode/delete_plan.html', {'plan':plan})

def deleteTask(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect('darkboard')

def deletePlan(request, pk):
    plan = Plan.objects.get(id=pk)
    plan.delete()
    return redirect('darkboard')


def statistics(request):
    # Get the number of tasks from the database
    num_plans = Plan.objects.filter(user=request.user)
    num_tasks = []
    for plan in num_plans:
        tasks = Task.objects.filter(plan=plan)
        for task in tasks:
            num_tasks.append(task)
    
    context = {'num_tasks': num_tasks}
    return render(request, 'darkmode/statistics.html', context)



@login_required
def task_list(request):
    tasks = Task.objects.filter(plan__user=request.user)
    return render(request, 'darkmode/task_list.html', {'tasks': tasks})


@login_required
def profile(request):
   return render(request, "darkmode/profile.html")

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
        return redirect('profile2')

    return render(request, 'darkmode/update_profile.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Updating the session with the new password
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile2')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'darkmode/change_password.html', {'form': form})