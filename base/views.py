from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from .models import Blog, Comment, User
from .forms import BlogForm, UserForm, MyUserCreationForm


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''     
    blogs = Blog.objects.filter(
        Q(title__icontains=q) |
        Q(topic__name__icontains=q) |
        Q(body__icontains=q)
    )
    context = {'blogs': blogs}
    return render(request, 'base/home.html', context)

def blog(request, pk):
    blog = Blog.objects.get(id=pk)
    comments = Comment.objects.filter(blog=blog)
    context = {'blog': blog, 'comments': comments}
    return render(request, 'base/blog.html', context)

@login_required(login_url='login')
def createBlog(request):
    form = BlogForm()

    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request, 'base/blog_form.html', context)

@login_required(login_url='login')
def updateBlog(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.user != blog.author:
        return redirect('home')
    form = BlogForm(instance=blog)

    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog', pk=pk)

    context = {'form': form}
    return render(request, 'base/blog_form.html', context)

@login_required(login_url='login')
def deleteBlog(request, pk):
    blog = Blog.objects.get(id=pk)
    if request.user != blog.author:
        return redirect('home')
    if request.method == 'POST':
        blog.delete()
        return redirect('home')
    
    context = {'obj': blog}
    return render(request, 'base/delete.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password is incorrect')
            return redirect('login')
    page = 'login'
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')  

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, f'An error occurred during registration {form.errors.as_data()}')
        
    page = 'register'
    context = {'page': page, 'form': form }
    return render(request, 'base/login_register.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    blogs = user.blog_set.all()
    context = {'user': user, 'blogs': blogs}
    return render(request, 'base/profile.html', context)

def updateProfile(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)

    context = {'form': form}
    return render(request, 'base/update_user.html', context)