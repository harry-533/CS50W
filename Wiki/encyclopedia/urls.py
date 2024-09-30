from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry"),
    path("search/", views.search_results, name="search_results"),
    path("new/", views.new_page , name="new_page"),
    path("edit/", views.edit, name="edit"),
    path("random/", views.random_entry, name="random")
]
