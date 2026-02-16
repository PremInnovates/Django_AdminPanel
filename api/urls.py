"""
URL configuration for ChargeNow API.
"""
from django.urls import path
from .views.auth_views import LoginView, UserRegisterView, OperatorRegisterView , ForgotPasswordView 
from .views.user_views import (
    UserProfileView,
    UserVehicleListView, UserVehicleDetailView,
    UserRequestListView, UserRequestDetailView,
    UserBookingListView, UserBookingCancelView,
    UserPaymentView, UserFeedbackView,
    TrackOperatorView
)
from .views.operator_views import (
    OperatorProfileView, OperatorStatusView,
    OperatorVanView,
    OperatorRequestListView, OperatorRequestActionView,
    OperatorChargingView,
    OperatorBookingHistoryView, OperatorPaymentHistoryView, OperatorFeedbackHistoryView
)
from django.views.generic import RedirectView
urlpatterns = [
    #  AUTH ENDPOINTS 
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/user/register/', UserRegisterView.as_view(), name='user-register'),
    path('auth/operator/register/', OperatorRegisterView.as_view(), name='operator-register'),
    path('auth/forgot-password/', ForgotPasswordView.as_view()),
    
    # path('user/vehicles/', UserVehicleListView.as_view(), name='user-vehicles'),
    # path('user/vehicles/<int:vehicle_id>/', UserVehicleDetailView.as_view(), name='user-vehicle-detail'),
    
    #path('', RedirectView.as_view(url='/admin-dashboard/', permanent=False)),
    path('user/profile/', UserProfileView.as_view(), name='user-profile'),
    # Vehicles
    path('user/vehicles/', UserVehicleListView.as_view(), name='user-vehicles'),
    path('user/vehicles/<int:vehicle_id>/', UserVehicleDetailView.as_view(), name='user-vehicle-detail'),
    # Requests
    path('user/requests/', UserRequestListView.as_view(), name='user-requests'),
    path('user/requests/<int:request_id>/', UserRequestDetailView.as_view(), name='user-request-detail'),
    # Bookings
    path('user/bookings/', UserBookingListView.as_view(), name='user-bookings'),
    path('user/bookings/<int:booking_id>/cancel/', UserBookingCancelView.as_view(), name='user-booking-cancel'),
    # Payments
    path('user/payments/', UserPaymentView.as_view(), name='user-payments'),
    # Feedback
    path('user/feedback/', UserFeedbackView.as_view(), name='user-feedback'),
    # Track Operator
    path('user/track-operator/<int:operator_id>/', TrackOperatorView.as_view(), name='track-operator'),
    
    # ========== OPERATOR ENDPOINTS ==========
    path('operator/profile/', OperatorProfileView.as_view(), name='operator-profile'),
    path('operator/status/', OperatorStatusView.as_view(), name='operator-status'),
    path('operator/van/', OperatorVanView.as_view(), name='operator-van'),
    # Requests
    path('operator/requests/', OperatorRequestListView.as_view(), name='operator-requests'),
    path('operator/requests/<int:request_id>/', OperatorRequestActionView.as_view(), name='operator-request-action'),
    # Charging
    path('operator/charging/<int:booking_id>/', OperatorChargingView.as_view(), name='operator-charging'),
    # History
    path('operator/bookings/', OperatorBookingHistoryView.as_view(), name='operator-bookings'),
    path('operator/payments/', OperatorPaymentHistoryView.as_view(), name='operator-payments'),
    path('operator/feedback/', OperatorFeedbackHistoryView.as_view(), name='operator-feedback'),


]
