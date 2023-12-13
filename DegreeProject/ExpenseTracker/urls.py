from django.urls import path, include
from . import views
from .views import RegisterView
from django.contrib.auth import views as auth_views
from ExpenseTracker.views import CustomLoginView  
from ExpenseTracker.forms import LoginForm
from django.urls import re_path


urlpatterns = [
    path('', views.WelcomePage, name='welcome'),
    path('InfoPage/', views.info_page, name='InfoPage'),
    path('expense-tracker/', views.expense_tracker, name='expense_tracker'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='ExpenseTracker/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='ExpenseTracker/logout.html'), name='logout'),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    path('add-category/', views.add_category, name='add_category'),
    path('AddExpense/', views.AddExpense, name='AddExpense'),
]

