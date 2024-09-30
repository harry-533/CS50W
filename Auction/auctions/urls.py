from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("view/<int:id>/", views.view_listing, name="view"),
    path("watchlist", views.watchlists, name="watchlist"),
    path("category", views.category, name="category")
]

