from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Follower

from network.helpers.decorators import is_authenticated


def index(request):
    posts = Post.objects.all().order_by("-created_at")

    return render(
        request,
        "network/index.html",
        {"posts": posts, "title_page": "All Posts", "show_new_post": True},
    )


@is_authenticated
def following(request):
    logged_user = User.objects.get(id=request.user.id)
    posts = []

    for user_id in logged_user.following.values_list("follower_id", flat=True):
        user = User.objects.get(id=user_id)
        posts.extend(Post.objects.filter(user=user))

    return render(
        request,
        "network/index.html",
        {"posts": posts, "title_page": "Following Posts", "show_new_post": False},
    )


@is_authenticated
def profile(request, user_id=""):
    follow_button = "Follow"
    user = User.objects.get(id=request.user.id)
    logged_user = user
    posts = Post.objects.filter(user=request.user).all().order_by("-created_at")

    if user_id != "":
        user = User.objects.get(id=user_id)
        if Follower.objects.filter(follower=user, following=logged_user).exists():
            follow_button = "Unfollow"

        posts = Post.objects.filter(user=user_id).all().order_by("-created_at")

    return render(
        request,
        "network/profile.html",
        {"posts": posts, "user_info": user, "follow_button": follow_button},
    )


def follow(request, user_id_to_follow=""):
    label_button = "Unfollow"
    logged_user = User.objects.get(id=request.user.id)
    target_user = User.objects.get(id=user_id_to_follow)
    follower = Follower.objects.get_or_create(
        follower=target_user, following=logged_user
    )

    if not follower[1]:
        Follower.objects.get(follower=target_user, following=logged_user).delete()
        label_button = "Follow"

    return JsonResponse(
        {
            "label_button": label_button,
            "followers": target_user.follower.count(),
            "following": target_user.following.count(),
        }
    )


def post(request, post_id=""):
    # create a new post
    if request.method == "POST":
        content_post = request.POST["new-post"]
        if content_post == "":
            return HttpResponseRedirect(reverse("index"))
        user = User.objects.get(username=request.user.username)
        new_post = Post.objects.create(content=content_post, user=user)
        new_post.save()

    # remove post with post id
    if post_id != "":
        post = Post.objects.get(id=post_id)
        post.delete()

    return HttpResponseRedirect(reverse("index"))


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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
