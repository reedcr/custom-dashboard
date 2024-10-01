from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [ 
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('accounts/profile/', login_required(views.profile_view), name='profile'),
    path("dashboard_manager/", login_required(views.dashboard_manager), name="dashboard_manager"),
    path("dashboard_customer/", login_required(views.dashboard_customer), name="dashboard_customer"),
    path("finance_month/<int:yr>/<int:month>/", login_required(views.finance_month), name="finance_month"),
    path("finance_unit/<int:yr>/", login_required(views.finance_unit), name="finance_unit"),
    path('submit_add_income/', login_required(views.submit_add_income), name='submit_add_income'),
    path('submit_update_income/<int:income_id>/', login_required(views.submit_update_income), name='submit_update_income'),
    path('submit_delete_income/<int:income_id>/', login_required(views.submit_delete_income), name='submit_delete_income'),
    path('submit_add_expense/', login_required(views.submit_add_expense), name='submit_add_expense'),
    path('submit_update_expense/<int:expense_id>/', login_required(views.submit_update_expense), name='submit_update_expense'),
    path('submit_delete_expense/<int:expense_id>/', login_required(views.submit_delete_expense), name='submit_delete_expense'),
    path("export_to_csv/", login_required(views.export_to_csv), name="export_to_csv"),
    path("submit_payment/<int:payment_id>/", login_required(views.submit_payment), name="submit_payment"),
    path("service_request/<int:service_id>/", login_required(views.service_request), name="service_request")
]