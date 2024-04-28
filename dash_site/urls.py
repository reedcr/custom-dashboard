from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [ 
    path("", views.index, name="index"),
    # path("login", views.login, name="login"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('accounts/profile/', login_required(views.profile_view), name='profile'),
    path("dashboard/", login_required(views.dashboard), name="dashboard"),
    path("finance_month/<int:yr>/<int:month>/", login_required(views.finance_month), name="finance_month"),
    path("finance_unit/<int:yr>/", login_required(views.finance_unit), name="finance_unit"),
    path("export_to_csv/", login_required(views.export_to_csv), name="export_to_csv"),
    path('insert_new_income/', login_required(views.insert_new_income), name='insert_new_income'),
    path('update_income/<int:income_id>', login_required(views.update_income), name='update_income'),
    path('delete_income/<int:income_id>', login_required(views.delete_income), name='delete_income'),
    path('insert_new_expense/', login_required(views.insert_new_expense), name='insert_new_expense'),
    path('update_expense/<int:expense_id>', login_required(views.update_expense), name='update_expense'),
    path('delete_expense/<int:expense_id>', login_required(views.delete_expense), name='delete_expense'),
]