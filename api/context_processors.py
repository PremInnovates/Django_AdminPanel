from django.utils import timezone
from api.models import User, Booking, ChargingVan, Payment, Request, Feedback, UserVehicle, VanOperator

def admin_dashboard_counts(request):
    # Dashboard ke liye real-time data
    if request.path.startswith('/admin/'):
        try:
            # Total counts
            total_users = User.objects.count()
            total_vans = ChargingVan.objects.filter(is_active=True).count()
            total_bookings = Booking.objects.count()
            total_payments = Payment.objects.filter(status='completed').count()
            pending_requests = Request.objects.filter(status='pending').count()
            total_feedbacks = Feedback.objects.count()
            total_vehicles = UserVehicle.objects.count()
            total_operators = VanOperator.objects.count()
            
            # Today's stats
            today = timezone.now().date()
            today_bookings = Booking.objects.filter(booking_date__date=today).count()
            
            today_payments = Payment.objects.filter(
                payment_date__date=today,
                status='completed'
            )
            today_revenue = sum([p.amount for p in today_payments])
            
            return {
                'dashboard_counts': {
                    'total_users': total_users,
                    'total_vans': total_vans,
                    'total_bookings': total_bookings,
                    'total_payments': total_payments,
                    'pending_requests': pending_requests,
                    'total_feedbacks': total_feedbacks,
                    'total_vehicles': total_vehicles,
                    'total_operators': total_operators,
                    'today_bookings': today_bookings,
                    'today_revenue': today_revenue,
                }
            }
        except Exception as e:
            print(f"Error in context processor: {e}")
            return {'dashboard_counts': {}}
    return {}