from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entry, name="name"),
    path('new', views.new, name='new'),
    path('wiki/<str:name>/edit', views.edit, name='edit'),
    path('random', views.randompage, name='random'),
    path('search', views.search, name='search'),
]
