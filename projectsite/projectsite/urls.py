from django.contrib import admin
from django.urls import path

from landingpage.views import HomePageView, RoomList, RoomUpdateView, ServiceList, ServiceUpdateView, BedList, BedUpdateView, OccupantList, OccupantUpdateView, RegistrationList, RegistrationUpdateView, BillingList, BillingUpdateView
from landingpage import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),
    path('room_list', RoomList.as_view(), name='RoomList'),
    path('room_list/add', views.add_room, name='RoomAdd'),
    path('room_list/<pk>', RoomUpdateView.as_view(), name="RoomUpdate"),
    path('service_list', ServiceList.as_view(), name='ServiceList'),
    path('service_list/add', views.add_service, name='ServiceAdd'),
    path('service_list/<pk>', ServiceUpdateView.as_view(), name="ServiceUpdate"),
    path('bed_list', BedList.as_view(), name='BedList'),
    path('bed_list/add', views.add_bed, name='BedAdd'),
    path('bed_list/<pk>', BedUpdateView.as_view(), name="BedUpdate"),
    path('occupant_list', OccupantList.as_view(), name='OccupantList'),
    path('occupant_list/add', views.add_occupant, name='OccupantAdd'),
    path('occupant_list/<pk>', OccupantUpdateView.as_view(), name="OccupantUpdate"),
    path('registration_list', RegistrationList.as_view(), name='RegistrationList'),
    path('registration_list/add', views.add_registration, name='RegistrationAdd'),
    path('registration_list/<pk>', RegistrationUpdateView.as_view(), name="RegistrationUpdate"),
    path('billing_list', BillingList.as_view(), name='BillingList'),
    path('billing_list/add', views.add_billing, name='BillingAdd'),
    path('billing_list/<pk>', BillingUpdateView.as_view(), name="BillingUpdate"),


]
