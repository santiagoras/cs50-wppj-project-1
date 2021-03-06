from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.read_entry, name="wiki"),
    path("contribution", views.write_entry, name="write"),
    path("edit/<str:entry>", views.edit_entry, name="edit"),
    path("random", views.random_entry, name="random")
]
