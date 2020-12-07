from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tutors", views.tutors, name="tutors"),
    path("categories/<int:category_id>", views.category, name="category"),
    path("create", views.create, name="create"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("listings/<int:listing_id>/bid", views.bid, name="bid"),
    path("listings/<int:listing_id>/close", views.close, name="close"),
    path("listings/<int:listing_id>/comment", views.comment, name="comment"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("users/<int:user_id>", views.profile, name="profile"),
    path("users/<int:user_id>/edit", views.edit_profile, name="edit_profile"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add", views.watchlist_add, name="watchlist_add"),
    path("watchlist/delete", views.watchlist_delete, name="watchlist_delete"),
    path("listings_won", views.listings_won, name="listings_won")
]
