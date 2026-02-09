from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from api.models import User, VanOperator, ChargingVan, Booking

# @staff_member_required
# def admin_dashboard(request):
#     context = {
#         "total_users": User.objects.count(),
#         "total_operators": VanOperator.objects.count(),
#         "total_vans": ChargingVan.objects.count(),
#         "total_bookings": Booking.objects.count(),
#     }
    # return render(request, "admin/index.html", context)
