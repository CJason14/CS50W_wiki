from unicodedata import name
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="item"),
    path("rand", views.rand, name="rand"),
    path("newpage", views.newpage, name="newpage"),
    path("editpage/<str:title>", views.editpage, name="editpage"),
    path("search", views.search, name="search")
]
