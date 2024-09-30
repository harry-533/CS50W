from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.core.paginator import Paginator

from .models import *


def index(request):
    postList = Post.objects.all().order_by('-id')
    p = Paginator(postList, 10)
    page =request.GET.get('page')
    posts = p.get_page(page)

    if request.method == "POST":
        if 'postContent' in request.POST:
            content = request.POST["postContent"]
            newPost = Post(username = request.user.username, user_id = request.user.id, body = content)
            newPost.save()
            return HttpResponseRedirect(reverse("index"))
        elif 'postEdit' in request.POST:
            content = request.POST.get("postEdit")
            editedPost = Post.objects.get(id = request.POST.get('postId'))
            editedPost.body = content
            editedPost.save()
            return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "network/index.html", {
            'posts': posts
        })
    
def following(request):
    postList = Post.objects.all().order_by('-id')
    p = Paginator(postList, 10)
    page =request.GET.get('page')
    posts = p.get_page(page)

    if not request.user.id:
       return HttpResponseRedirect(reverse("login"))
     
    return render(request, "network/following.html", {
        'posts': posts
    })


def profile(request, id):
    userProfile = User.objects.get(id = id)
    if userProfile.id in request.user.following:
        following = 'Unfollow'
    else:
        following = 'Follow'

    if request.method == "POST":
        followUser = request.user
        if following == 'Follow':
            followUser.following.append(userProfile.id)
            followUser.save()
            userProfile.followerCount += 1
            userProfile.save()
            following = 'Unfollow'
        else:
            followUser.following.remove(userProfile.id)
            followUser.save()
            userProfile.followerCount -= 1
            userProfile.save()
            following = 'Follow'

    return render(request, "network/profile.html", {
        'profile': userProfile,
        'follow': following,
        'posts': Post.objects.filter(user_id = userProfile.id).order_by('-id')
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
@csrf_exempt
@login_required
def toggle_like(request, post_id):
    post = Post.objects.get(pk=post_id)

    user = request.user

    if user.id in post.liked_by:
        post.liked_by.remove(user.id)
        post.likes -= 1
        liked = False
    else:
        post.liked_by.append(user.id)
        post.likes += 1
        liked = True

    post.save()

    return JsonResponse({
        'liked': liked,
        'like_count': post.likes
    })