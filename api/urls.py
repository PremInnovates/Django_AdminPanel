"""
URL configuration for ChargeNow API.
"""
from django.urls import path
from .views.auth_views import LoginView, UserRegisterView, OperatorRegisterView , ForgotPasswordView 
from .views.user_views import UserVehicleListView, UserVehicleDetailView
from django.views.generic import RedirectView
urlpatterns = [
    #  AUTH ENDPOINTS 
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/user/register/', UserRegisterView.as_view(), name='user-register'),
    path('auth/operator/register/', OperatorRegisterView.as_view(), name='operator-register'),
    path('auth/forgot-password/', ForgotPasswordView.as_view()),
    path('user/vehicles/', UserVehicleListView.as_view(), name='user-vehicles'),
    path('user/vehicles/<int:vehicle_id>/', UserVehicleDetailView.as_view(), name='user-vehicle-detail'),
    
    #path('', RedirectView.as_view(url='/admin-dashboard/', permanent=False)),
]
