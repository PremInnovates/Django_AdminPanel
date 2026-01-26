from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.http import JsonResponse
from django.contrib.auth.models import Group, User as DjangoUser
from django import forms
from django.db import models

from .models import (
    User, VanOperator, ChargingVan,
    UserVehicle, Request, Booking, Payment, Feedback
)


# CUSTOM ADMIN SITE

class ChargeNowAdminSite(admin.AdminSite):
    site_header = "ChargeNow Admin"
    site_title = "ChargeNow Admin"
    index_title = "Dashboard"

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({
            "total_users": User.objects.count(),
            "total_operators": VanOperator.objects.count(),
            "total_vans": ChargingVan.objects.count(),
            "total_user_vehicles": UserVehicle.objects.count(),
            "total_requests": Request.objects.count(),
            "total_bookings": Booking.objects.count(),
            "total_payments": Payment.objects.count(),
            "total_feedbacks": Feedback.objects.count(),
        })
        return super().index(request, extra_context)


admin_site = ChargeNowAdminSite(name="chargenow_admin")


# REMOVE DEFAULT DJANGO MODELS

for model in [DjangoUser, Group]:
    try:
        admin_site.unregister(model)
    except admin.sites.NotRegistered:
        pass


# AJAX DELETE VIEW

@admin_site.admin_view
def ajax_delete(request):
    model_name = request.POST.get("model")
    obj_id = request.POST.get("id")

    model_map = {
        "user": User,
        "operator": VanOperator,
        "van": ChargingVan,
        "uservehicle": UserVehicle,
        "request": Request,
        "booking": Booking,
        "payment": Payment,
        "feedback": Feedback,
    }

    model = model_map.get(model_name)
    if model:
        model.objects.filter(pk=obj_id).delete()

    return JsonResponse({"success": True})


# BASE ADMIN -DELETE HEADER FIX HERE 

class AjaxDeleteAdmin(admin.ModelAdmin):

    class Media:
        js = (
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "admin/js/custom_delete.js",
        )

    def delete_action(self, obj):
        return format_html(
            '<a href="#" class="delete-btn" data-model="{}" data-id="{}">'
            '<i class="fa fa-trash" style="color:red;"></i></a>',
            self.model._meta.model_name,
            obj.pk
        )

    delete_action.short_description = "Delete"  

    def has_add_permission(self, request):
        return False


# CHARGING VAN FORM

class ChargingVanForm(forms.ModelForm):
    class Meta:
        model = ChargingVan
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["operator"].widget = forms.Select()


# USER ADMIN

class UserAdmin(AjaxDeleteAdmin):
    list_display = (
        "user_id",
        "user_name",
        "user_email",
        "user_phone",
        "created_at",
        "delete_action",
    )
    list_filter = ("user_email",)
    search_fields = ("user_name",)

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return False


# VAN OPERATOR ADMIN

class VanOperatorAdmin(AjaxDeleteAdmin):
    list_display = (
        "operator_id",
        "operator_name",
        "operator_email",
        "operator_phone",
        "operator_status",
        "is_verified",
        "created_at",
        "delete_action",
    )

    list_editable = ("is_verified",)
    readonly_fields = ("operator_status",)
    list_filter = ("is_verified",)
    search_fields = ("operator_name",)

    def has_add_permission(self, request):
        return True


# CHARGING VAN ADMIN

class ChargingVanAdmin(AjaxDeleteAdmin):
    list_display = (
        "van_id",
        "van_number",
        "operator",
        "battery_capacity",
        "created_at",
        "delete_action",
    )

    list_editable = ("operator",)

    formfield_overrides = {
        models.ForeignKey: {"widget": forms.Select},
    }

    search_fields = ("van_number",)
    list_filter = ("operator",)

    def has_add_permission(self, request):
        return True


# OTHER ADMINS

class UserVehicleAdmin(AjaxDeleteAdmin):
    list_display = (
        "vehicle_id",
        "vehicle_company",
        "vehicle_model",
        "vehicle_number",
        "user",
        "created_at",
        "delete_action",
        
    )
    search_fields = ("vehicle_number",)
   

class RequestAdmin(AjaxDeleteAdmin):
    list_display = (
        "request_id",
        "user",
        "operator",
        "vehicle",
        "request_time",
        "user_latitude",
        "user_longitude",
        "request_status",
        "delete_action",
    )
    list_filter = ("request_status",)

class BookingAdmin(AjaxDeleteAdmin):
    list_display = (
        "booking_id",
        "booking_status",
        "operator",
        "request_id",
        "created_at",
        "delete_action",
    )
    list_filter = ("booking_status",)
    

# class PaymentAdmin(AjaxDeleteAdmin):
#     list_display = (
#         "payment_id",
#         "amount",
#         "p_method",
#         "payment_time",
#         "p_status",
#         "delete_action",
#     )
#     list_filter = ("p_method",)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'payment_id',
        'user',
        'operator',
        'booking',
        'amount',
        'p_method',
        'p_status',
        'payment_time'
    )    
    def get_user(self, obj):
        return obj.user.user_name

    def get_operator(self, obj):
        return obj.operator.operator_name

    def get_booking(self, obj):
        return obj.booking.booking_id


    



class FeedbackAdmin(AjaxDeleteAdmin):
    list_display = (
        "feedback_id",
        "user",
        "operator",
        "rating",
        "comments",
        "delete_action",
    )


# REGISTER AJAX URL

admin_site.get_urls = lambda: [
    path("api/delete/", admin_site.admin_view(ajax_delete)),
] + admin.AdminSite.get_urls(admin_site)


# REGISTER MODELS

admin_site.register(User, UserAdmin)
admin_site.register(VanOperator, VanOperatorAdmin)
admin_site.register(ChargingVan, ChargingVanAdmin)
admin_site.register(UserVehicle, UserVehicleAdmin)
admin_site.register(Request, RequestAdmin)
admin_site.register(Booking, BookingAdmin)
admin_site.register(Payment, PaymentAdmin)
admin_site.register(Feedback, FeedbackAdmin)
