from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .models import Todo
from .forms import RegisterForm, TodoForm 
from django.db.models import F
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView

# Create your views here.
def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        
    else:
        form = RegisterForm()
        
    return render(request, 'registration/register.html', {'form': form})


def custom_logout(request):
    # Log the user out and clear the session
    logout(request)
    request.session.flush()  # Ensure all session data is deleted
    return redirect('/')  # Redirect to the home page


def todo_list(request):
    sort_by = request.GET.get('sort_by', 'due_date')  # Default to due_date
    todos = Todo.objects.filter(user=request.user, is_completed=False).order_by(
        F(sort_by).asc()
    )
    return render(request, 'todos/todo_list.html', {'todos': todos})
def add_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        
        if form.is_valid:
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todo')
    else:
        form = TodoForm()
    return render(request, 'todos/add_todo.html', {'form': form})


def update_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todos/update_todo.html', {'form': form})


def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect('todo')
    return render(request, 'todos/delete_todo.html', {'todo': todo})


def todo_detail(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    return render(request, 'todos/todo_detail.html', {'todo': todo})


def mark_as_complete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.is_completed = True
    todo.completed_at = timezone.now()
    todo.save()
    return redirect('todo')

def completed_todos(request):
    todos = Todo.objects.filter(user=request.user, is_completed=True).order_by('-completed_at')
    return render(request, 'todos/completed_todos.html', {'todos': todos})


@login_required
def profile(request):
    return render(request, "users/profile.html", {'user': request.user})

@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('home')  # Redirect to the homepage or login page after deletion
    return render(request, 'users/delete_profile.html')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'  # Customize template if needed
    success_url = reverse_lazy('custom_success_page')
    success_message = "Your password was changed successfully!"
    
    
def password_change_success(request):
    return render(request, 'registration/password_change_done.html')





