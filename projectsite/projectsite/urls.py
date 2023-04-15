from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path


from landingpage.views import HomePageView, RoomList, RoomUpdateView, ServiceList, ServiceUpdateView, BedList 
from landingpage.views import BedUpdateView, OccupantList, OccupantUpdateView, RegistrationList, RegistrationUpdateView
from landingpage.views import RegistrationRegView, BillingList, BillingUpdateView, OccupantView, PaymentList
from landingpage.views import PaymentUpdateView, OccupantViewBillingUpdate, DashMaleVacantBed, DashFemaleVacantBed
from landingpage.views import DashForeignVacantBed, OccupantViewPaymentUpdate, DemeritList, DemeritUpdateView
from landingpage.views import OccupantDemeritList, OccupantDemeritUpdateView, OccupantViewDemeritUpdate, OccupantAccounts
from landingpage.views import OccupantAccountsUpdateView, user_login_view, user_logout_view, admin_login_view, admin_logout_view
from landingpage.views import AdminList, AdminUpdateView, RegMonthRep, RegYearRep, OccMonthRep, OccYearRep, RoomListCard, RoomCardUpdateView

from landingpage.views import FDHomePageView, FDDashMaleVacantBed, FDDashFemaleVacantBed, FDDashForeignVacantBed
from landingpage.views import FDRegistrationList, FDRegistrationUpdateView, FDRegistrationRegView, FDRegMonthRep, FDRegYearRep
from landingpage.views import FDOccupantList, FDOccupantUpdateView, FDOccupantView, FDOccMonthRep, FDOccYearRep


from landingpage import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    url('^searchableselect/', include('searchableselect.urls')),
    path('admin/', admin.site.urls),

    # start of Superadmin URL
    path('', views.HomePageView.as_view(), name='home'),

    path('dash_male_vacant_bed', DashMaleVacantBed.as_view(), name='DashMaleVacantBed'),
    path('dash_female_vacant_bed', DashFemaleVacantBed.as_view(), name='DashFemaleVacantBed'),
    path('dash_foreign_vacant_bed', DashForeignVacantBed.as_view(), name='DashForeignVacantBed'),

    path('registration_list', RegistrationList.as_view(), name='RegistrationList'),
    path('registration_list/add', views.add_registration, name='RegistrationAdd'),
    path('registration_list/<pk>', RegistrationUpdateView.as_view(), name="RegistrationUpdate"),
    path('registration_view/registration_list/<pk>', RegistrationUpdateView.as_view(), name="RegistrationUpdate"),
    path('registration_view/<pk>', RegistrationRegView.as_view(), name="RegistrationView"),
    path('registration_list/<int:pk>/', views.RegPDF, name='RegPDF'),
    path('registration_view/registration_list/<int:pk>/', views.RegPDF, name='RegPDF'),
    path('occupant_view/registration_view/<pk>', RegistrationRegView.as_view(), name="RegistrationView"),

    path('reg_all_csv', views.reg_all_csv, name="reg_all_csv"),
    path('reg_month_csv', views.reg_month_csv, name="reg_month_csv"),
    path('reg_year_csv', views.reg_year_csv, name="reg_year_csv"),
    path('reg_month_rep/registration_list', RegMonthRep.as_view(), name='RegMonthRep'),
    path('reg_year_rep/registration_list', RegYearRep.as_view(), name='RegYearRep'),

    path('occupant_list', OccupantList.as_view(), name='OccupantList'),
    path('occupant_list/add', views.add_occupant, name='OccupantAdd'),
    path('occupant_list/renew', views.renew_occupant, name='OccupantRenew'),
    path('occupant_list/<pk>', OccupantUpdateView.as_view(), name="OccupantUpdate"),
    path('occupant_view/<pk>', OccupantView.as_view(), name="OccupantView"),
    path('occupant_view/occupant_list/<pk>', OccupantUpdateView.as_view(), name="OccupantUpdate"),
    path('occupant_view/billing_list/<pk>', OccupantViewBillingUpdate.as_view(), name="OccupantViewBillingUpdate"),
    path('occupant_list/<int:pk>/', views.OccPDF, name='OccPDF'),
    path('occupant_view/occupant_list/<int:pk>/', views.OccPDF, name='OccPDF'),
    path('occupant_view/payment_list/<pk>', OccupantViewPaymentUpdate.as_view(), name="OccupantViewPaymentUpdate"),

    path('occ_all_csv', views.occ_all_csv, name="occ_all_csv"),
    path('occ_month_csv', views.occ_month_csv, name="occ_month_csv"),
    path('occ_year_csv', views.occ_year_csv, name="occ_year_csv"),
    path('occ_month_rep/occupant_list', OccMonthRep.as_view(), name='OccMonthRep'),
    path('occ_year_rep/occupant_list', OccYearRep.as_view(), name='OccYearRep'),

    path('billing_list', BillingList.as_view(), name='BillingList'),
    path('billing_list/add', views.add_billing, name='BillingAdd'),
    path('billing_list/<pk>', BillingUpdateView.as_view(), name="BillingUpdate"),
    path('other_add/', views.other_add_billing, name='other-add'),
    path('other_update/<billing_id>', views.other_update_billing, name='other-update'),

    path('payment_list', PaymentList.as_view(), name='PaymentList'),
    path('payment_list/add', views.add_payment, name='PaymentAdd'),
    path('payment_list/<pk>', PaymentUpdateView.as_view(), name="PaymentUpdate"),

    path('occupant_demerit_list', OccupantDemeritList.as_view(), name='OccupantDemeritList'),
    path('occupant_demerit_list/add', views.add_occupant_demerit, name='OccupantDemeritAdd'),
    path('occupant_demerit_list/<pk>', OccupantDemeritUpdateView.as_view(), name="OccupantDemeritUpdate"),
    path('occupant_view/occupant_demerit_list/<pk>', OccupantViewDemeritUpdate.as_view(), name="OccupantViewDemeritUpdate"),
    
    path('room_list', RoomList.as_view(), name='RoomList'),
    path('room_list_card', RoomListCard.as_view(), name='RoomListCard'),
    path('room_list/add', views.add_room, name='RoomAdd'),
    path('room_list/<pk>', RoomUpdateView.as_view(), name="RoomUpdate"),
    path('room_list_card/<pk>', RoomCardUpdateView.as_view(), name="RoomCardUpdate"),

    path('bed_list', BedList.as_view(), name='BedList'),
    path('bed_list/add', views.add_bed, name='BedAdd'),
    path('bed_list/<pk>', BedUpdateView.as_view(), name="BedUpdate"),

    path('service_list', ServiceList.as_view(), name='ServiceList'),
    path('service_list/add', views.add_service, name='ServiceAdd'),
    path('service_list/<pk>', ServiceUpdateView.as_view(), name="ServiceUpdate"),

    path('demerit_list', DemeritList.as_view(), name='DemeritList'),
    path('demerit_list/add', views.add_demerit, name='DemeritAdd'),
    path('demerit_list/<pk>', DemeritUpdateView.as_view(), name="DemeritUpdate"),

    path('AdminNotifications/', views.AdminNotifications, name='AdminNotifications'),

    path('users', OccupantAccounts.as_view(), name='OccupantAccounts'),
    path('users/<pk>', OccupantAccountsUpdateView.as_view(), name="OccupantAccountsUpdate"),

    path('admin_list', AdminList.as_view(), name='AdminList'),
    path('admin_list/add', views.add_admin, name='AdminAdd'),
    path('admin_list/<pk>', AdminUpdateView.as_view(), name="AdminUpdate"),

    path('admin_profile', views.AdminProfile.as_view(), name='AdminProfile'),
    path('admin_profile/<pk>', views.AdminProfileUpdateView.as_view(), name='AdminProfileUpdateView'),
    # end of Superadmin URL

    # start of Frontdesk URL
    path('fd_home', views.FDHomePageView.as_view(), name='fd_home'),

    path('fd_dash_male_vacant_bed', FDDashMaleVacantBed.as_view(), name='FDDashMaleVacantBed'),
    path('fd_dash_female_vacant_bed', FDDashFemaleVacantBed.as_view(), name='FDDashFemaleVacantBed'),
    path('fd_dash_foreign_vacant_bed', FDDashForeignVacantBed.as_view(), name='FDDashForeignVacantBed'),

    path('fd_registration_list', FDRegistrationList.as_view(), name='FDRegistrationList'),
    path('fd_registration_list/add', views.fd_add_registration, name='FDRegistrationAdd'),
    path('fd_registration_list/<pk>', FDRegistrationUpdateView.as_view(), name="FDRegistrationUpdate"),
    path('fd_registration_view/fd_registration_list/<pk>', FDRegistrationUpdateView.as_view(), name="FDRegistrationUpdate"),
    path('fd_registration_view/<pk>', FDRegistrationRegView.as_view(), name="FDRegistrationView"),
    path('fd_registration_list/<int:pk>/', views.FDRegPDF, name='FDRegPDF'),
    path('fd_registration_view/fd_registration_list/<int:pk>/', views.FDRegPDF, name='FDRegPDF'),
    path('fd_occupant_view/fd_registration_view/<pk>', FDRegistrationRegView.as_view(), name="FDRegistrationView"),

    path('fd_reg_all_csv', views.fd_reg_all_csv, name="fd_reg_all_csv"),
    path('fd_reg_month_csv', views.fd_reg_month_csv, name="fd_reg_month_csv"),
    path('fd_reg_year_csv', views.fd_reg_year_csv, name="fd_reg_year_csv"),
    path('fd_reg_month_rep/fd_registration_list', FDRegMonthRep.as_view(), name='FDRegMonthRep'),
    path('fd_reg_year_rep/fd_registration_list', FDRegYearRep.as_view(), name='FDRegYearRep'),

    path('fd_occupant_list', FDOccupantList.as_view(), name='FDOccupantList'),
    path('fd_occupant_list/add', views.fd_add_occupant, name='FDOccupantAdd'),
    path('fd_occupant_list/renew', views.fd_renew_occupant, name='FDOccupantRenew'),
    path('fd_occupant_list/<pk>', FDOccupantUpdateView.as_view(), name="FDOccupantUpdate"),
    path('fd_occupant_view/<pk>', FDOccupantView.as_view(), name="FDOccupantView"),
    path('fd_occupant_view/fd_occupant_list/<pk>', FDOccupantUpdateView.as_view(), name="FDOccupantUpdate"),
    path('fd_occupant_list/<int:pk>/', views.FDOccPDF, name='FDOccPDF'),
    path('fd_occupant_view/fd_occupant_list/<int:pk>/', views.FDOccPDF, name='FDOccPDF'),

    path('fd_occ_all_csv', views.fd_occ_all_csv, name="fd_occ_all_csv"),
    path('fd_occ_month_csv', views.fd_occ_month_csv, name="fd_occ_month_csv"),
    path('fd_occ_year_csv', views.fd_occ_year_csv, name="fd_occ_year_csv"),
    path('fd_occ_month_rep/fd_occupant_list', FDOccMonthRep.as_view(), name='FDOccMonthRep'),
    path('fd_occ_year_rep/fd_occupant_list', FDOccYearRep.as_view(), name='FDOccYearRep'),
    # end of Frontdesk URL

    path('admin_login/', admin_login_view, name="admin_login"),
    path('admin_logout/', admin_logout_view, name="logout"),
    path('admin_forgot_password/', views.admin_forgot_password_form, name='admin_forgot_password'),
    path('admin_security_question/', views.admin_security_question_form, name='admin_security_question'),
    path('admin_show_password/', views.admin_show_password_form, name='admin_show_password'),

    # path('delete_occupant/<int:id>', views.delete_occupant, name='delete_occupant'),
    # path('delete_bed/<int:id>', views.delete_bed, name='delete_bed'),
    # path('delete_room/<int:id>', views.delete_room, name='delete_room'),
    # path('delete_reg/<int:id>', views.delete_reg, name='delete_reg'),
    # path('delete_demerit/<int:id>', views.delete_demerit, name='delete_demerit'),
    # path('delete_user/<int:id>', views.delete_user, name='delete_user'),


    # start of User URL
    path('user_login/', user_login_view, name="user_login"),
    path('user_logout/', user_logout_view, name="user_logout"),

    path('user_forgot_password/', views.user_forgot_password_form, name='user_forgot_password'),
    path('user_security_question/', views.user_security_question_form, name='user_security_question'),
    path('user_show_password/', views.user_show_password_form, name='user_show_password'),

    path('user_dashboard', views.User_Dashboard.as_view(), name='UserDashboard'),
    path('user_profile', views.User_Profile.as_view(), name='UserProfile'),
    path('user_account', views.User_Account.as_view(), name='UserAccount'),
    path('user_account/<pk>', views.User_AccountUpdateView.as_view(), name='UserAccountUpdateView'),
    path('user_billing', views.User_Billing.as_view(), name='UserBilling'),
    path('user_billing/<pk>', views.User_Contract_View.as_view(), name='User_Contract_View'),

    path('user_services', views.User_Services.as_view(), name='UserServices'),
    path('user_service_avail/add', views.user_add_billing, name='UserAvailService'),
    path('user_service_other/', views.user_other_add_billing, name='user_other_add'),

    path('OccupantNotifications/', views.OccupantNotifications, name='OccupantNotifications'),
    # end of User URL

]
