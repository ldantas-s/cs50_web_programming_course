from django.urls import path

from . import views

app_name = 'airline_flights'
urlpatterns = [
  path('', views.index, name='index'),
  path('<int:flight_id>', views.flight, name='flight')
]