from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.read_entry, name="read_entry"),
    path("<str:entry>", views.write_entry, name="write_entry")
]
