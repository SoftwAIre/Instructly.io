from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    # path("create_post", views.create_post, name="create_post"),
    # path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    # path("profile/<int:user_id>", views.profile, name="profile"),
    # # left the below path long.
    # path("profile/<int:user_id>/toggle_following", views.toggle_following, name="toggle_following"),
    # path("following", views.following, name="following"),
    # path("like/<int:post_id>", views.like, name="like"),
    # path("login", views.login_view, name="login"),
    # path("logout", views.logout_view, name="logout"),
    # path("register", views.register, name="register")
]
