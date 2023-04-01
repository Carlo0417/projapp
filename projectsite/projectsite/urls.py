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
from landingpage.views import AdminList, AdminUpdateView, RegMonthRep, RegYearRep, OccMonthRep, OccYearRep
from landingpage.views import FrontDeskRegistrationList, FrontDeskRegistrationUpdateView, FrontDeskRegistrationRegView
from landingpage.views import FrontDeskRegMonthRep, FrontDeskRegYearRep, FrontDeskOccupantList, FrontDeskOccupantUpdateView, FrontDeskOccupantView
from landingpage.views import FrontDeskOccMonthRep, FrontDeskOccYearRep, FrontDeskOccupantDemeritList, FrontDeskOccupantDemeritUpdateView
from landingpage.views import FrontDeskRoomList, FrontDeskRoomUpdateView, FrontDeskOccupantViewDemeritUpdate, FrontDeskBedList, FrontDeskBedUpdateView
from landingpage.views import FrontDeskServiceList, FrontDeskServiceUpdateView, FrontDeskDemeritList, FrontDeskDemeritUpdateView
from landingpage.views import AccountingServiceList, AccountingPaymentList, AccountingPaymentUpdateView, AccountingBillingList, AccountingBillingUpdateView
from landingpage.views import AccountingOccupantList, AccountingOccupantView, RoomListCard, RoomCardUpdateView

from landingpage import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    url('^searchableselect/', include('searchableselect.urls')),
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),
    
    path('room_list', RoomList.as_view(), name='RoomList'),
    path('room_list_card', RoomListCard.as_view(), name='RoomListCard'),
    path('room_list/add', views.add_room, name='RoomAdd'),
    path('room_list/<pk>', RoomUpdateView.as_view(), name="RoomUpdate"),
    path('room_list_card/<pk>', RoomCardUpdateView.as_view(), name="RoomCardUpdate"),

    path('service_list', ServiceList.as_view(), name='ServiceList'),
    path('service_list/add', views.add_service, name='ServiceAdd'),
    path('service_list/<pk>', ServiceUpdateView.as_view(), name="ServiceUpdate"),

    path('bed_list', BedList.as_view(), name='BedList'),
    path('bed_list/add', views.add_bed, name='BedAdd'),
    path('bed_list/<pk>', BedUpdateView.as_view(), name="BedUpdate"),
    path('dash_male_vacant_bed', DashMaleVacantBed.as_view(), name='DashMaleVacantBed'),
    path('dash_female_vacant_bed', DashFemaleVacantBed.as_view(), name='DashFemaleVacantBed'),
    path('dash_foreign_vacant_bed', DashForeignVacantBed.as_view(), name='DashForeignVacantBed'),

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


    path('user_service_avail/add', views.user_add_billing, name='UserAvailService'),
    path('user_service_other/', views.user_other_add_billing, name='user_other_add'),

    path('admin_login/', admin_login_view, name="admin_login"),
    path('admin_logout/', admin_logout_view, name="logout"),
    path('admin_list', AdminList.as_view(), name='AdminList'),
    path('admin_list/add', views.add_admin, name='AdminAdd'),
    path('admin_list/<pk>', AdminUpdateView.as_view(), name="AdminUpdate"),

    path('delete_occupant/<int:id>', views.delete_occupant, name='delete_occupant'),
    path('delete_bed/<int:id>', views.delete_bed, name='delete_bed'),
    path('delete_room/<int:id>', views.delete_room, name='delete_room'),
    path('delete_reg/<int:id>', views.delete_reg, name='delete_reg'),
    # path('delete_demerit/<int:id>', views.delete_demerit, name='delete_demerit'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),

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
    
    path('AdminNotifications/', views.AdminNotifications, name='AdminNotifications'),

    path('OccupantNotifications/', views.OccupantNotifications, name='OccupantNotifications'),

    path('admin_forgot_password/', views.admin_forgot_password_form, name='admin_forgot_password'),
    path('admin_security_question/', views.admin_security_question_form, name='admin_security_question'),
    path('admin_show_password/', views.admin_show_password_form, name='admin_show_password'),

    # Occupant Account URL
    path('user_login/', user_login_view, name="user_login"),
    path('user_logout/', user_logout_view, name="user_logout"),

    path('user_forgot_password/', views.user_forgot_password_form, name='user_forgot_password'),
    path('user_security_question/', views.user_security_question_form, name='user_security_question'),
    path('user_show_password/', views.user_show_password_form, name='user_show_password'),

    path('user_dashboard', views.User_Dashboard.as_view(), name='UserDashboard'),
    path('user_services', views.User_Services.as_view(), name='UserServices'),
    path('user_profile', views.User_Profile.as_view(), name='UserProfile'),
    path('user_account', views.User_Account.as_view(), name='UserAccount'),
    path('user_account/<pk>', views.User_AccountUpdateView.as_view(), name='UserAccountUpdateView'),
    path('user_billing', views.User_Billing.as_view(), name='UserBilling'),
    path('user_billing/<pk>', views.User_Contract_View.as_view(), name='User_Contract_View'),
    # end of Occupant Account URL


    #Front Desk URLs
    path('frontdesk_home', views.FrontDeskHomePageView.as_view(), name='frontdesk_home'),
    path('frontdesk_registration_list', FrontDeskRegistrationList.as_view(), name='FrontDeskRegistrationList'),
    path('frontdesk_registration_list/add', views.front_desk_add_registration, name='FrontDeskRegistrationAdd'),
    path('frontdesk_registration_list/<pk>', FrontDeskRegistrationUpdateView.as_view(), name="FrontDeskRegistrationUpdateView"),
    path('frontdesk_registration_view/frontdesk_registration_list/<pk>', FrontDeskRegistrationUpdateView.as_view(), name="FrontDeskRegistrationUpdate"),
    path('frontdesk_registration_view/<pk>', FrontDeskRegistrationRegView.as_view(), name="FrontDeskRegistrationRegView"),
    path('frontdesk_registration_list/<int:pk>/', views.frontdesk_RegPDF, name='frontdesk_RegPDF'),
    path('frontdesk_registration_view/frontdesk_registration_list/<int:pk>/', views.frontdesk_RegPDF, name='frontdesk_RegPDF'),
    path('frontdesk_reg_all_csv', views.frontdesk_reg_all_csv, name="frontdesk_reg_all_csv"),
    path('frontdesk_reg_month_csv', views.frontdesk_reg_month_csv, name="frontdesk_reg_month_csv"),
    path('frontdesk_reg_year_csv', views.frontdesk_reg_year_csv, name="frontdesk_reg_year_csv"),
    path('frontdesk_reg_month_rep/frontdesk_registration_list', FrontDeskRegMonthRep.as_view(), name='FrontDeskRegMonthRep'),
    path('frontdesk_reg_year_rep/frontdesk_registration_list', FrontDeskRegYearRep.as_view(), name='FrontDeskRegYearRep'),

    path('frontdesk_occupant_list', FrontDeskOccupantList.as_view(), name='FrontDeskOccupantList'),
    path('frontdesk_occupant_list/add', views.frontdesk_add_occupant, name='FrontDeskOccupantAdd'),
    path('frontdesk_occupant_list/renew', views.frontdesk_renew_occupant, name='FrontDeskOccupantRenew'),
    path('frontdesk_occupant_list/<pk>', FrontDeskOccupantUpdateView.as_view(), name="FrontDeskOccupantUpdate"),
    path('frontdesk_occupant_view/<pk>', FrontDeskOccupantView.as_view(), name="FrontDeskOccupantView"),
    path('frontdesk_occupant_view/frontdesk_occupant_list/<pk>', FrontDeskOccupantUpdateView.as_view(), name="FrontDeskOccupantUpdate"),
    path('frontdesk_occ_all_csv', views.frontdesk_occ_all_csv, name="frontdesk_occ_all_csv"),
    path('frontdesk_occ_month_csv', views.frontdesk_occ_month_csv, name="frontdesk_occ_month_csv"),
    path('frontdesk_occ_year_csv', views.frontdesk_occ_year_csv, name="frontdesk_occ_year_csv"),
    path('frontdesk_occ_month_rep/frontdesk_occupant_list', FrontDeskOccMonthRep.as_view(), name='FrontDeskOccMonthRep'),
    path('frontdesk_occ_year_rep/frontdesk_occupant_list', FrontDeskOccYearRep.as_view(), name='FrontDeskOccYearRep'),
    path('frontdesk_occupant_list/<int:pk>/', views.FrontDeskOccPDF, name='FrontDeskOccPDF'),
    path('frontdesk_occupant_view/frontdesk_occupant_list/<int:pk>/', views.FrontDeskOccPDF, name='FrontDeskOccPDF'),
    path('frontdesk_occupant_view/frontdesk_registration_view/<pk>', FrontDeskRegistrationRegView.as_view(), name="FrontDeskRegistrationView"),
    path('frontdesk_occupant_view/frontdesk_occupant_demerit_list/<pk>', FrontDeskOccupantViewDemeritUpdate.as_view(), name="FrontDeskOccupantViewDemeritUpdate"),

    path('frontdesk_occupant_demerit_list', FrontDeskOccupantDemeritList.as_view(), name='FrontDeskOccupantDemeritList'),
    path('frontdesk_occupant_demerit_list/add', views.frontdesk_add_occupant_demerit, name='FrontDeskOccupantDemeritAdd'),
    path('frontdesk_occupant_demerit_list/<pk>', FrontDeskOccupantDemeritUpdateView.as_view(), name="FrontDeskOccupantDemeritUpdate"),

    path('frontdesk_room_list', FrontDeskRoomList.as_view(), name='FrontDeskRoomList'),
    path('frontdesk_room_list/add', views.frontdesk_add_room, name='FrontDeskRoomAdd'),
    path('frontdesk_room_list/<pk>', FrontDeskRoomUpdateView.as_view(), name="FrontDeskRoomUpdate"),

    path('frontdesk_bed_list', FrontDeskBedList.as_view(), name='FrontDeskBedList'),
    path('frontdesk_bed_list/add', views.frontdesk_add_bed, name='FrontDeskBedAdd'),
    path('frontdesk_bed_list/<pk>', FrontDeskBedUpdateView.as_view(), name="FrontDeskBedUpdate"),

    path('frontdesk_service_list', FrontDeskServiceList.as_view(), name='FrontDeskServiceList'),
    path('frontdesk_service_list/add', views.frontdesk_add_service, name='FrontDeskServiceAdd'),
    path('frontdesk_service_list/<pk>', FrontDeskServiceUpdateView.as_view(), name="FrontDeskServiceUpdate"),

    path('frontdesk_demerit_list', FrontDeskDemeritList.as_view(), name='FrontDeskDemeritList'),
    path('frontdesk_demerit_list/add', views.frontdesk_add_demerit, name='FrontDeskDemeritAdd'),
    path('frontdesk_demerit_list/<pk>', FrontDeskDemeritUpdateView.as_view(), name="FrontDeskDemeritUpdate"),

    path('FrontDeskAdminNotifications/', views.FrontDeskAdminNotifications, name='FrontDeskAdminNotifications'),

    path('frontdesk_admin_profile', views.FrontDeskAdminProfile.as_view(), name='FrontDeskAdminProfile'),
    path('frontdesk_admin_profile/<pk>', views.FrontDeskAdminProfileUpdateView.as_view(), name='FrontDeskAdminProfileUpdateView'),
    # end of Front Desk URLs

    #Accounting Staff URLs
    path('accounting_home', views.AccountingHomePageView.as_view(), name='accounting_home'),

    path('AccountingAdminNotifications/', views.AccountingAdminNotifications, name='AccountingAdminNotifications'),

    path('accounting_admin_profile', views.AccountingAdminProfile.as_view(), name='AccountingAdminProfile'),
    path('accounting_admin_profile/<pk>', views.AccountingAdminProfileUpdateView.as_view(), name='AccountingAdminProfileUpdateView'),

    path('accounting_service_list', AccountingServiceList.as_view(), name='AccountingServiceList'),

    path('accounting_payment_list', AccountingPaymentList.as_view(), name='AccountingPaymentList'),
    path('accounting_payment_list/add', views.accounting_add_payment, name='AccountingPaymentAdd'),
    path('accounting_payment_list/<pk>', AccountingPaymentUpdateView.as_view(), name="AccountingPaymentUpdate"),

    path('accounting_billing_list', AccountingBillingList.as_view(), name='AccountingBillingList'),
    path('accounting_billing_list/add', views.accounting_add_billing, name='AccountingBillingAdd'),
    path('accounting_billing_list/<pk>', AccountingBillingUpdateView.as_view(), name="AccountingBillingUpdate"),
    path('accounting_other_add/', views.accounting_other_add_billing, name='accounting-other-add'),
    path('accounting_other_update/<billing_id>', views.accounting_other_update_billing, name='accounting-other-update'),

    path('accounting_occupant_list', AccountingOccupantList.as_view(), name='AccountingOccupantList'),

    # path('accounting_occ_all_csv', views.accounting_occ_all_csv, name="accounting_occ_all_csv"),
    # path('accounting_occ_month_csv', views.accounting_occ_month_csv, name="accounting_occ_month_csv"),
    # path('accounting_occ_year_csv', views.accoutning_occ_year_csv, name="accounting_occ_year_csv"),

    # path('accounting_occ_month_rep/accounting_occupant_list', AccountingOccMonthRep.as_view(), name='AccountingOccMonthRep'),
    # path('accounting_occ_year_rep/accounting_occupant_list', AccountingOccYearRep.as_view(), name='AccountingOccYearRep'),

    path('accounting_occupant_list/<int:pk>/', views.AccountingOccPDF, name='AccountingOccPDF'),
    # path('accounting_occupant_view/accounting_occupant_list/<int:pk>/', views.AccountingOccPDF, name='AccountingOccPDF'),

    path('admin_profile', views.AdminProfile.as_view(), name='AdminProfile'),
    path('admin_profile/<pk>', views.AdminProfileUpdateView.as_view(), name='AdminProfileUpdateView'),

    path('accounting_occupant_view/<pk>', AccountingOccupantView.as_view(), name="AccountingOccupantView"),

]
