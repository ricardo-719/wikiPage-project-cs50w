from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create_entry, name="create"),
    path("edit", views.edit_entry, name="edit"),
    path("search", views.search_page, name="searchPage"),
    path("<str:name>", views.read_page, name="readPage")
    
]
