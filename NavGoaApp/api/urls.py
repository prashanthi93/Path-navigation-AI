from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.getData,name="all-data"),
    path('post/',views.postData,name="post-data"),
]