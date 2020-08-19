from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.
def logout_view(request):
    """Log the user out."""
    logout(request)
    return HttpResponseRedirect(reverse('blog:index'))

def register(request):
    """Register a new user."""
    if request.method != 'POST':
        #Display blank registration form.
        form = UserCreationForm()
    else:
        #Process completed form.
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Log the user in then redirect to home page.
            authenticated_user = authenticate(username=new_user.username,
                password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('blog:index'))

    context = {'form': form}
    return render(request, 'users/register.html', context)

def profile(request, user_id):
    user_profile = User.objects.get(id=user_id)
    user_name = user_profile.username
    user_date_joined = user_profile.date_joined
    user_posts = user_profile.blogpost_set.all()
    user_comments = user_profile.postcomment_set.all()
    context={'username': user_name, 'date_joined': user_date_joined, 
        'posts': user_posts, 'comments': user_comments}
    return render(request, 'users/view_profile.html', context)