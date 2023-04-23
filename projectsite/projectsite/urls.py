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
from landingpage.views import FDOccupantDemeritList, FDOccupantDemeritUpdateView, FDOccupantViewDemeritUpdate
from landingpage.views import FDRoomList, FDRoomUpdateView, FDRoomListCard, FDRoomCardUpdateView, FDBedList, FDBedUpdateView
from landingpage.views import FDServiceList, FDServiceUpdateView, FDDemeritList, FDDemeritUpdateView

from landingpage.views import ASHomePageView, ASDashMaleVacantBed, ASDashFemaleVacantBed, ASDashForeignVacantBed
from landingpage.views import ASOccupantList, ASOccupantView, ASOccMonthRep, ASOccYearRep, ASBillingList
from landingpage.views import ASOccupantList, ASOccupantView, ASOccMonthRep, ASOccYearRep
from landingpage.views import ASPaymentList, ASServiceList

from landingpage.views import DMHomePageView, DMDashMaleVacantBed, DMDashFemaleVacantBed, DMDashForeignVacantBed
from landingpage.views import DMRegistrationList, DMRegistrationRegView, DMRegMonthRep, DMRegYearRep
from landingpage.views import DMOccupantList, DMOccupantView, DMOccMonthRep, DMOccYearRep, DMBillingList, DMPaymentList
from landingpage.views import DMOccupantDemeritList, DMRoomList, DMRoomListCard, DMBedList, DMServiceList, DMDemeritList
from landingpage.views import DMOccupantAccounts, DMOccupantAccountsUpdateView


from landingpage import views

from django.contrib.auth import views as auth_views

from django.views.generic import TemplateView

urlpatterns = [
    url('^searchableselect/', include('searchableselect.urls')),
    path('admin/', admin.site.urls),

    # start of Super Admin URL
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
    # end of SuperAadmin URL

    # start of Front Desk URL
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

    path('fd_occupant_demerit_list', FDOccupantDemeritList.as_view(), name='FDOccupantDemeritList'),
    path('fd_occupant_demerit_list/add', views.fd_add_occupant_demerit, name='FDOccupantDemeritAdd'),
    path('fd_occupant_demerit_list/<pk>', FDOccupantDemeritUpdateView.as_view(), name="FDOccupantDemeritUpdate"),
    path('fd_occupant_view/fd_occupant_demerit_list/<pk>', FDOccupantViewDemeritUpdate.as_view(), name="FDOccupantViewDemeritUpdate"),

    path('fd_room_list', FDRoomList.as_view(), name='FDRoomList'),
    path('fd_room_list_card', FDRoomListCard.as_view(), name='FDRoomListCard'),
    path('fd_room_list/add', views.fd_add_room, name='FDRoomAdd'),
    path('fd_room_list/<pk>', FDRoomUpdateView.as_view(), name="FDRoomUpdate"),
    path('fd_room_list_card/<pk>', FDRoomCardUpdateView.as_view(), name="FDRoomCardUpdate"),

    path('fd_bed_list', FDBedList.as_view(), name='FDBedList'),
    path('fd_bed_list/add', views.fd_add_bed, name='FDBedAdd'),
    path('fd_bed_list/<pk>', FDBedUpdateView.as_view(), name="FDBedUpdate"),

    path('fd_service_list', FDServiceList.as_view(), name='FDServiceList'),
    path('fd_service_list/add', views.fd_add_service, name='FDServiceAdd'),
    path('fd_service_list/<pk>', FDServiceUpdateView.as_view(), name="FDServiceUpdate"),

    path('fd_demerit_list', FDDemeritList.as_view(), name='FDDemeritList'),
    path('fd_demerit_list/add', views.fd_add_demerit, name='FDDemeritAdd'),
    path('fd_demerit_list/<pk>', FDDemeritUpdateView.as_view(), name="FDDemeritUpdate"),

    path('FDAdminNotifications/', views.FDAdminNotifications, name='FDAdminNotifications'),

    path('fd_admin_profile', views.FDAdminProfile.as_view(), name='FDAdminProfile'),
    path('fd_admin_profile/<pk>', views.FDAdminProfileUpdateView.as_view(), name='FDAdminProfileUpdateView'),
    # end of Front Desk URL

    # start of Accounting Staff URL
    path('as_home', views.ASHomePageView.as_view(), name='as_home'),

    path('as_dash_male_vacant_bed', ASDashMaleVacantBed.as_view(), name='ASDashMaleVacantBed'),
    path('as_dash_female_vacant_bed', ASDashFemaleVacantBed.as_view(), name='ASDashFemaleVacantBed'),
    path('as_dash_foreign_vacant_bed', ASDashForeignVacantBed.as_view(), name='ASDashForeignVacantBed'),

    path('as_occupant_list', ASOccupantList.as_view(), name='ASOccupantList'),
    path('as_occupant_view/<pk>', ASOccupantView.as_view(), name="ASOccupantView"),
    path('as_occupant_list/<int:pk>/', views.ASOccPDF, name='ASOccPDF'),
    path('as_occupant_views/as_occupant_list/<int:pk>/', views.ASOccPDF, name='ASOccPDF'),

    path('as_occ_all_csv', views.as_occ_all_csv, name="as_occ_all_csv"),
    path('as_occ_month_csv', views.as_occ_month_csv, name="as_occ_month_csv"),
    path('as_occ_year_csv', views.as_occ_year_csv, name="as_occ_year_csv"),
    path('as_occ_month_rep/as_occupant_list', ASOccMonthRep.as_view(), name='ASOccMonthRep'),
    path('as_occ_year_rep/as_occupant_list', ASOccYearRep.as_view(), name='ASOccYearRep'),

    path('as_billing_list', ASBillingList.as_view(), name='ASBillingList'),
    path('as_billing_list/add', views.as_add_billing, name='ASBillingAdd'),
    path('as_other_add/', views.as_other_add_billing, name='as_other-add'),
    
    path('as_payment_list', ASPaymentList.as_view(), name='ASPaymentList'),
    path('as_payment_list/add', views.as_add_payment, name='ASPaymentAdd'),

    path('as_service_list', ASServiceList.as_view(), name='ASServiceList'),

    path('ASAdminNotifications/', views.ASAdminNotifications, name='ASAdminNotifications'),

    path('as_admin_profile', views.ASAdminProfile.as_view(), name='ASAdminProfile'),
    path('as_admin_profile/<pk>', views.ASAdminProfileUpdateView.as_view(), name='ASAdminProfileUpdateView'),
    # end of Accounting Staff URL

    # start of Dorm Manager URL
    path('dm_home', views.DMHomePageView.as_view(), name='dm_home'),

    path('dm_dash_male_vacant_bed', DMDashMaleVacantBed.as_view(), name='DMDashMaleVacantBed'),
    path('dm_dash_female_vacant_bed', DMDashFemaleVacantBed.as_view(), name='DMDashFemaleVacantBed'),
    path('dm_dash_foreign_vacant_bed', DMDashForeignVacantBed.as_view(), name='DMDashForeignVacantBed'),

    path('dm_registration_list', DMRegistrationList.as_view(), name='DMRegistrationList'),
    path('dm_registration_view/<pk>', DMRegistrationRegView.as_view(), name="DMRegistrationView"),
    path('dm_occupant_view/dm_registration_view/<pk>', DMRegistrationRegView.as_view(), name="DMRegistrationView"),

    path('dm_reg_month_rep/dm_registration_list', DMRegMonthRep.as_view(), name='DMRegMonthRep'),
    path('dm_reg_year_rep/dm_registration_list', DMRegYearRep.as_view(), name='DMRegYearRep'),

    path('dm_occupant_list', DMOccupantList.as_view(), name='DMOccupantList'),
    path('dm_occupant_view/<pk>', DMOccupantView.as_view(), name="DMOccupantView"),
    path('dm_occ_month_rep/dm_occupant_list', DMOccMonthRep.as_view(), name='DMOccMonthRep'),
    path('dm_occ_year_rep/dm_occupant_list', DMOccYearRep.as_view(), name='DMOccYearRep'),
    path('dm_occupant_view/dm_occupant_list/<pk>', DMOccupantView.as_view(), name="DMOccupantView"),

    path('dm_billing_list', DMBillingList.as_view(), name='DMBillingList'),

    path('dm_payment_list', DMPaymentList.as_view(), name='DMPaymentList'),

    path('dm_occupant_demerit_list', DMOccupantDemeritList.as_view(), name='DMOccupantDemeritList'),

    path('dm_room_list', DMRoomList.as_view(), name='DMRoomList'),
    path('dm_room_list_card', DMRoomListCard.as_view(), name='DMRoomListCard'),

    path('dm_bed_list', DMBedList.as_view(), name='DMBedList'),

    path('dm_service_list', DMServiceList.as_view(), name='DMServiceList'),

    path('dm_demerit_list', DMDemeritList.as_view(), name='DMDemeritList'),

    path('DMAdminNotifications/', views.DMAdminNotifications, name='DMAdminNotifications'),

    path('dm_users', DMOccupantAccounts.as_view(), name='DMOccupantAccounts'),
    path('dm_users/<pk>', DMOccupantAccountsUpdateView.as_view(), name="DMOccupantAccountsUpdate"),

    path('dm_admin_profile', views.DMAdminProfile.as_view(), name='DMAdminProfile'),
    path('dm_admin_profile/<pk>', views.DMAdminProfileUpdateView.as_view(), name='DMAdminProfileUpdateView'),
    # end of Dorm Manager URL

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

    path('user_rules/', views.UserRules, name='UserRules'),
    # end of User URL

]
