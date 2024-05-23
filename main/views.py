from django.shortcuts import render, redirect, get_object_or_404
from .forms import Registaraionform, PostForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from .models import Post
from django.contrib.auth.models import User, Group


# Create your views here.
@login_required(login_url='/login')
def home(request):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        user_id = request.POST.get('user_id')
        profile_id = request.POST.get('profile_id')


        if post_id:
            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm('main.delete_post')):
                post.delete()
        elif user_id:
            user = User.objects.filter(pk=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except:
                    pass

                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass
        elif profile_id:
            return redirect('user_profile', username=profile_id)
    posts = Post.objects.all()

    return render(request, 'main/homepage.html', {'posts':posts})


@login_required(login_url='/login')
def user_profile(request, username):
    # Retrieve the user object based on the username passed in the URL
    user = get_object_or_404(User, username=username)
    
    # Fetch all the posts associated with that user
    posts = Post.objects.filter(author=user)
    
    # Render the user_profile.html template with the posts
    return render(request, 'main/user_profile.html', {'user': user, 'posts': posts})






@permission_required('main.add_post', login_url='/login', raise_exception=True)
@login_required(login_url='/login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/home')
    else:
        form = PostForm(request.POST)
        return render(request, 'main/create_post.html', {'form':form})



@login_required(login_url='/login')
def show_dashboard(request):
    # Filter posts by the currently logged-in user
    posts = Post.objects.filter(author=request.user)
    return render(request, 'main/dashboard.html', {'posts': posts})






def signup(request):
    if request.method == 'POST':
        form = Registaraionform(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = Registaraionform()
    return render(request, 'main/signup.html', {'form': form})