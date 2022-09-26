from django.contrib import admin
from django.urls import path

from landingpage.views import HomePageView, RoomList, RoomUpdateView
from landingpage import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),
    path('room_list', RoomList.as_view(), name='RoomList'),
    path('room_list/add', views.add_room, name='RoomAdd'),
    path('room_list/<pk>', RoomUpdateView.as_view(), name="RoomUpdate"),
]
