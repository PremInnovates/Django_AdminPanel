from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.http import JsonResponse
from django.contrib.auth.models import Group, User as DjangoUser
from django import forms
from django.db import models
from django.http import HttpResponseForbidden

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
        "vanoperator": VanOperator,
        "chargingvan": ChargingVan,
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
    actions = None   #  DEFAULT DELETE DROPDOWN REMOVE

    class Media:
        js = (
            "https://code.jquery.com/jquery-3.6.0.min.js",
            "admin/js/custom_delete.js",
        )

    def delete_action(self, obj):
        return format_html(
            '<a href="#" class="delete-btn" data-model="{}" data-id="{}" title="Delete">'
            '<i class="fas fa-trash text-danger"></i>'
            '</a>',
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
        "user_address", 
        "created_at",
        "delete_action",
    )
    list_filter = ("user_email",)
    search_fields = ("user_name",)
    readonly_fields = ("role",)
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
        "operator_license", 
        "is_verified",
        "created_at",
        "delete_action",
    )
    
    list_filter = ("is_verified", "operator_status")    
    #  Password is Display as ****
    formfield_overrides = {
        models.CharField: {"widget": forms.TextInput(attrs={"size": "50"})},
    }

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)

        
        if db_field.name == "operator_password":
            formfield.widget = forms.PasswordInput(render_value=True)
            formfield.widget.attrs.update({
                "autocomplete": "new-password",
            })

        return formfield

    list_filter = ("is_verified", "operator_status")
    readonly_fields = ("role","operator_status")
   
    search_fields = (
        "operator_name",
        "operator_email",
        "operator_phone",
        "operator_license",
    )
    def has_add_permission(self, request):
        return True
    
    def history_view(self, request, object_id, extra_context=None):
        return HttpResponseForbidden("History is disabled")
    


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
    list_filter = ("operator",)
    formfield_overrides = {
        models.ForeignKey: {"widget": forms.Select},
    }

    search_fields = (
        "van_number",
        "operator__operator_name",
    )
    def has_add_permission(self, request):
        return True


# OTHER ADMINS

class UserVehicleAdmin(AjaxDeleteAdmin):
    list_display = (
        "vehicle_id",
        "vehicle_company",
        "vehicle_name", 
        "vehicle_model",
        "vehicle_number",
        "user",
        "created_at",
        "delete_action",
        
    )
    search_fields = ("vehicle_number",)
    list_filter = ("vehicle_company",) 
   

class RequestAdmin(AjaxDeleteAdmin):
    list_display = (
        "request_id",
        "user",
        "operator",
        "vehicle",
        "user_latitude",
        "user_longitude",
        "request_status",
        "created_at", 
        "delete_action",
    )
    search_fields = ("user__user_name","operator__operator_name",)
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
    search_fields = ("operator__operator_name",)

class PaymentAdmin(AjaxDeleteAdmin):
    list_display = (
        'payment_id',
        'user',
        'operator',
        'booking',
        'amount',
        'payment_method',
        'payment_status',
        'created_at',
        'delete_action', 
    )    
    list_filter = ("payment_method","payment_status",) 
    def get_user(self, obj):
        return obj.user.user_name

    def get_operator(self, obj):
        return obj.operator.operator_name

    def get_booking(self, obj):
        return obj.booking.booking_id
    search_fields = ("user__user_name","operator__operator_name",)

class FeedbackAdmin(AjaxDeleteAdmin):
    list_display = (
        "feedback_id",
        "user",
        "operator",
        "rating",
        "comments",
        "created_at", 
        "delete_action",
    )
    list_filter = ("operator",) 
    search_fields = ("user__user_name","operator__operator_name",)

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