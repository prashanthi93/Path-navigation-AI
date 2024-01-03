from django.urls import path 

from . import views
urlpatterns = [
    path('',views.homePage,name="homepage"),
    path('map/<str:source>/<str:destination>/',views.mapPage, name = "mappage"),
    path('history/',views.historyPage,name='historypage'),
]