from django.conf.urls import url
from django.contrib import admin
from django.urls import path


from landingpage.views import HomePageView, RoomList, RoomUpdateView, ServiceList, ServiceUpdateView, BedList 
from landingpage.views import BedUpdateView, OccupantList, OccupantUpdateView, RegistrationList, RegistrationUpdateView
from landingpage.views import RegistrationRegView, BillingList, BillingUpdateView, OccupantView, PaymentList
from landingpage.views import PaymentUpdateView, OccupantViewBillingUpdate, MaleDormVacantBedList, FemaleDormVacantBedList
from landingpage.views import ForeignDormVacantBedList, OccupantViewPaymentUpdate, DemeritList, DemeritUpdateView
from landingpage.views import OccupantDemeritList, OccupantDemeritUpdateView, OccupantViewDemeritUpdate, OccupantAccounts
from landingpage.views import OccupantAccountsUpdateView, user_login_view, user_logout_view, User_Notifications, admin_login_view, admin_logout_view
from landingpage.views import AdminList, AdminUpdateView, RegMonthRep, RegYearRep, OccMonthRep, OccYearRep
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
    path('bed_list/add', views.add_bed, name='BedAdd'),
    path('bed_list/<pk>', BedUpdateView.as_view(), name="BedUpdate"),
    path('male_vacantbed', MaleDormVacantBedList.as_view(), name='MaleDormVacantBedList'),
    path('female_vacantbed', FemaleDormVacantBedList.as_view(), name='FemaleDormVacantBedList'),
    path('foreign_vacantbed', ForeignDormVacantBedList.as_view(), name='ForeignDormVacantBedList'),

    path('occupant_list', OccupantList.as_view(), name='OccupantList'),
    path('occupant_list/add', views.add_occupant, name='OccupantAdd'),
    path('occupant_list/renew', views.renew_occupant, name='OccupantRenew'),
    path('occupant_list/<pk>', OccupantUpdateView.as_view(), name="OccupantUpdate"),
    path('occupant_view/<pk>', OccupantView.as_view(), name="OccupantView"),
    path('occupant_view/occupant_list/<pk>', OccupantUpdateView.as_view(), name="OccupantUpdate"),
    path('occupant_view/billing_list/<pk>', OccupantViewBillingUpdate.as_view(), name="OccupantViewBillingUpdate"),
    path('occupant_list/<int:pk>/', views.OccPDF, name='OccPDF'),
    path('occupant_view/occupant_list/<int:pk>/', views.OccPDF, name='OccPDF'),

    path('registration_list', RegistrationList.as_view(), name='RegistrationList'),
    path('registration_list/add', views.add_registration, name='RegistrationAdd'),
    path('registration_list/<pk>', RegistrationUpdateView.as_view(), name="RegistrationUpdate"),
    path('registration_view/registration_list/<pk>', RegistrationUpdateView.as_view(), name="RegistrationUpdate"),
    path('registration_view/<pk>', RegistrationRegView.as_view(), name="RegistrationView"),
    path('registration_list/<int:pk>/', views.RegPDF, name='RegPDF'),
    path('registration_view/registration_list/<int:pk>/', views.RegPDF, name='RegPDF'),

    path('billing_list', BillingList.as_view(), name='BillingList'),
    path('billing_list/add', views.add_billing, name='BillingAdd'),
    path('billing_list/<pk>', BillingUpdateView.as_view(), name="BillingUpdate"),
    path('other_add/', views.other_add_billing, name='other-add'),
    path('other_update/<billing_id>', views.other_update_billing, name='other-update'),

    path('payment_list', PaymentList.as_view(), name='PaymentList'),
    path('payment_list/add', views.add_payment, name='PaymentAdd'),
    path('payment_list/<pk>', PaymentUpdateView.as_view(), name="PaymentUpdate"),

    path('demerit_list', DemeritList.as_view(), name='DemeritList'),
    path('demerit_list/add', views.add_demerit, name='DemeritAdd'),
    path('demerit_list/<pk>', DemeritUpdateView.as_view(), name="DemeritUpdate"),

    path('occupant_demerit_list', OccupantDemeritList.as_view(), name='OccupantDemeritList'),
    path('occupant_demerit_list/add', views.add_occupant_demerit, name='OccupantDemeritAdd'),
    path('occupant_demerit_list/<pk>', OccupantDemeritUpdateView.as_view(), name="OccupantDemeritUpdate"),

    path('occupant_view/registration_view/<pk>', RegistrationRegView.as_view(), name="RegistrationView"),
    path('occupant_view/payment_list/<pk>', OccupantViewPaymentUpdate.as_view(), name="OccupantViewPaymentUpdate"),
    path('occupant_view/occupant_demerit_list/<pk>', OccupantViewDemeritUpdate.as_view(), name="OccupantViewDemeritUpdate"),

    path('users', OccupantAccounts.as_view(), name='OccupantAccounts'),
    path('users/<pk>', OccupantAccountsUpdateView.as_view(), name="OccupantAccountsUpdate"),

    path('user_dashboard', views.User_Dashboard.as_view(), name='UserDashboard'),
    path('user_services', views.User_Services.as_view(), name='UserServices'),
    path('user_profile', views.User_Profile.as_view(), name='UserProfile'),
    path('user_account', views.User_Account.as_view(), name='UserAccount'),
    path('user_account/<pk>', views.User_AccountUpdateView.as_view(), name='UserAccountUpdateView'),
    path('user_billing', views.User_Billing.as_view(), name='UserBilling'),
    path('user_billing/<pk>', views.User_Contract_View.as_view(), name='User_Contract_View'),

    path('user_service_avail/add', views.user_add_billing, name='UserAvailService'),
    path('user_service_other/', views.user_other_add_billing, name='user_other_add'),

    path('user_notifications', views.User_Notifications.as_view(), name='UserNotifications'),


    path('admin_login/', admin_login_view, name="admin_login"),
    path('admin_logout/', admin_logout_view, name="logout"),
    path('admin_list', AdminList.as_view(), name='AdminList'),
    path('admin_list/add', views.add_admin, name='AdminAdd'),
    path('admin_list/<pk>', AdminUpdateView.as_view(), name="AdminUpdate"),

    path('delete_occupant/<int:id>', views.delete_occupant, name='delete_occupant'),
    # path('delete_bed/<int:id>', views.delete_bed, name='delete_bed'),
    path('delete_reg/<int:id>', views.delete_reg, name='delete_reg'),
    # path('delete_demerit/<int:id>', views.delete_demerit, name='delete_demerit'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),

    # url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout')

    path('reg_all_csv', views.reg_all_csv, name="reg_all_csv"),
    path('reg_month_csv', views.reg_month_csv, name="reg_month_csv"),
    path('reg_year_csv', views.reg_year_csv, name="reg_year_csv"),
    path('reg_month_rep/registration_list', RegMonthRep.as_view(), name='RegMonthRep'),
    path('reg_year_rep/registration_list', RegYearRep.as_view(), name='RegYearRep'),

    path('occ_all_csv', views.occ_all_csv, name="occ_all_csv"),
    path('occ_month_csv', views.occ_month_csv, name="occ_month_csv"),
    path('occ_year_csv', views.occ_year_csv, name="occ_year_csv"),
    path('occ_month_rep/occupant_list', OccMonthRep.as_view(), name='OccMonthRep'),
    path('occ_year_rep/occupant_list', OccYearRep.as_view(), name='OccYearRep'),

    path('user_login/', user_login_view, name="user_login"),
    path('user_logout/', user_logout_view, name="user_logout"),
    path('user_otp/', user_login_view, name='user_otp'),
    
    path('admin_notif_30th/', views.admin_notif_30th, name='admin_notif_30th'),

]
