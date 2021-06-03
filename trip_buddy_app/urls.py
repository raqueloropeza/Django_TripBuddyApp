from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register',views.register),
    path('login',views.login),
    path('logout',views.logout),
    path('dashboard',views.dashboardPage),
    path('trips/new',views.newPage),
    path('trips/create',views.createtrip),
    path('trips/<int:id>',views.tripPage),
    path('trips/edit/<int:id>', views.editTrip),
    path('trips/<int:id>/update', views.updatetrip),
    path('join/<int:id>',views.joinTrip),
    path('trips/delete/<int:id>', views.deletetrip),
    

]