from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("profile", views.profile, name="profile"),
    path("profile/<str:user_id>", views.profile, name="profile_follow"),
    path("follow/<str:user_id_to_follow>", views.follow, name="follow"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post", views.post, name="create_post"),
    path("post/<str:post_id>", views.post, name="delete_post"),
]
