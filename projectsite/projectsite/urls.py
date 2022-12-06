from django.conf.urls import url
from django.contrib import admin
from django.urls import path


from landingpage.views import HomePageView, RoomList, RoomUpdateView, ServiceList, ServiceUpdateView, BedList 
from landingpage.views import BedUpdateView, OccupantList, OccupantUpdateView, RegistrationList, RegistrationUpdateView
from landingpage.views import RegistrationRegView, BillingList, BillingUpdateView, OccupantView, PaymentList
from landingpage.views import PaymentUpdateView, OccupantViewBillingUpdate, MaleDormVacantBedList, FemaleDormVacantBedList
from landingpage.views import ForeignDormVacantBedList, OccupantViewPaymentUpdate, DemeritList, DemeritUpdateView
from landingpage.views import OccupantDemeritList, OccupantDemeritUpdateView, OccupantViewDemeritUpdate
from landingpage import views

from django.contrib.auth import views as auth_views

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
    path('male_vacantbed', MaleDormVacantBedList.as_view(), name='MaleDormVacantBedList'),
    path('female_vacantbed', FemaleDormVacantBedList.as_view(), name='FemaleDormVacantBedList'),
    path('foreign_vacantbed', ForeignDormVacantBedList.as_view(), name='ForeignDormVacantBedList'),
    path('bed_list/add', views.add_bed, name='BedAdd'),
    path('bed_list/<pk>', BedUpdateView.as_view(), name="BedUpdate"),
    path('occupant_list', OccupantList.as_view(), name='OccupantList'),
    path('occupant_list/add', views.add_occupant, name='OccupantAdd'),
    path('occupant_list/renew', views.renew_occupant, name='OccupantRenew'),
    path('occupant_list/<pk>', OccupantUpdateView.as_view(), name="OccupantUpdate"),
    path('occupant_view/<pk>', OccupantView.as_view(), name="OccupantView"),
    path('occupant_view/occupant_list/<pk>', OccupantUpdateView.as_view(), name="OccupantUpdate"),
    path('occupant_view/billing_list/<pk>', OccupantViewBillingUpdate.as_view(), name="OccupantViewBillingUpdate"),
    path('registration_list', RegistrationList.as_view(), name='RegistrationList'),
    path('registration_list/add', views.add_registration, name='RegistrationAdd'),
    path('registration_list/<pk>', RegistrationUpdateView.as_view(), name="RegistrationUpdate"),
    path('registration_view/registration_list/<pk>', RegistrationUpdateView.as_view(), name="RegistrationUpdate"),
    path('registration_view/<pk>', RegistrationRegView.as_view(), name="RegistrationView"),
    path('occupant_view/registration_view/<pk>', RegistrationRegView.as_view(), name="RegistrationView"),
    path('billing_list', BillingList.as_view(), name='BillingList'),
    path('billing_list/add', views.add_billing, name='BillingAdd'),
    path('billing_list/<pk>', BillingUpdateView.as_view(), name="BillingUpdate"),
    path('payment_list', PaymentList.as_view(), name='PaymentList'),
    path('payment_list/add', views.add_payment, name='PaymentAdd'),
    path('payment_list/<pk>', PaymentUpdateView.as_view(), name="PaymentUpdate"),
    path('occupant_view/payment_list/<pk>', OccupantViewPaymentUpdate.as_view(), name="OccupantViewPaymentUpdate"),
    path('demerit_list', DemeritList.as_view(), name='DemeritList'),
    path('demerit_list/add', views.add_demerit, name='DemeritAdd'),
    path('demerit_list/<pk>', DemeritUpdateView.as_view(), name="DemeritUpdate"),
    path('occupant_demerit_list', OccupantDemeritList.as_view(), name='OccupantDemeritList'),
    path('occupant_demerit_list/add', views.add_occupant_demerit, name='OccupantDemeritAdd'),
    path('occupant_demerit_list/<pk>', OccupantDemeritUpdateView.as_view(), name="OccupantDemeritUpdate"),
    path('occupant_view/occupant_demerit_list/<pk>', OccupantViewDemeritUpdate.as_view(), name="OccupantViewDemeritUpdate"),


    path('user_dashboard', views.User_Dashboard.as_view(), name='UserDashboard'),
    path('user_services', views.User_Services.as_view(), name='UserServices'),
    path('user_profile', views.User_Profile.as_view(), name='UserProfile'),
    path('user_account', views.User_Account.as_view(), name='UserAccount'),
    path('user_billing', views.User_Billing.as_view(), name='UserBilling'),


    # path('delete_occupant/<int:id>', views.delete_occupant, name='delete_occupant'),
    # path('delete_bed/<int:id>', views.delete_bed, name='delete_bed'),
    # path('delete_reg/<int:id>', views.delete_reg, name='delete_reg'),
    # path('delete_demerit/<int:id>', views.delete_demerit, name='delete_demerit'),

    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^user_login/$', auth_views.LoginView.as_view(template_name='user_login.html'), name='user_login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
]
