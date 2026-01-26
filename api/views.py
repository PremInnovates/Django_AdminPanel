from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .models import (
    User, VanOperator, ChargingVan,
    UserVehicle, Request, Booking, Payment, Feedback
)

@staff_member_required
def admin_dashboard(request):
    # Handle delete action
    delete_type = request.GET.get('delete_type')
    delete_id = request.GET.get('delete_id')

    if delete_type and delete_id:
        model_map = {
            "user": User,
            "operator": VanOperator,
            "van": ChargingVan,
            "uservehicle": UserVehicle,
            "request": Request,
            "booking": Booking,
            "payment": Payment,
            "feedback": Feedback
        }
        model = model_map.get(delete_type)
        if model:
            model.objects.filter(id=delete_id).delete()
            return redirect('admin_dashboard')

    # Debug print - Console mein dikhega
    print("=" * 50)
    print("DEBUG: Fetching data from database...")
    
    # Fetch counts for all models with debugging
    try:
        users_count = User.objects.count()
        operators_count = VanOperator.objects.count()
        vans_count = ChargingVan.objects.count()
        vehicles_count = UserVehicle.objects.count()
        requests_count = Request.objects.count()
        bookings_count = Booking.objects.count()
        payments_count = Payment.objects.count()
        feedbacks_count = Feedback.objects.count()
        
        print(f"Users: {users_count}")
        print(f"Operators: {operators_count}")
        print(f"Vans: {vans_count}")
        print(f"Vehicles: {vehicles_count}")
        print(f"Requests: {requests_count}")
        print(f"Bookings: {bookings_count}")
        print(f"Payments: {payments_count}")
        print(f"Feedbacks: {feedbacks_count}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        users_count = operators_count = vans_count = vehicles_count = 0
        requests_count = bookings_count = payments_count = feedbacks_count = 0

    # Fetch counts for all models
    context = {
        # Counts for dashboard cards
        "total_users": users_count,
        "total_operators": operators_count,
        "total_vans": vans_count,
        "total_vehicles": vehicles_count,
        "total_user_vehicles": vehicles_count,
        "total_requests": requests_count,
        "total_bookings": bookings_count,
        "total_payments": payments_count,
        "total_feedbacks": feedbacks_count,
    }
    
    print(f"Context sent: {context}")
    print("=" * 50)
    
    return render(request, "admin/index.html", context)