from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path('new-page/', views.new_page, name='new_page'),
    path('random-entry/', views.random_entry, name='random_entry'),
    path('edit-entry/<str:title>', views.edit_entry, name='edit_entry')
]
