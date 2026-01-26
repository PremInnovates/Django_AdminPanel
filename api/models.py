"""
Django models for ChargeNow database.
These models map to the existing MySQL tables.
"""

from django.db import models
from django.contrib.auth.hashers import make_password, check_password


# =========================
# USER MODEL
# =========================
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=30)
    user_email = models.EmailField(max_length=30, unique=True)
    user_password = models.CharField(max_length=255)
    user_phone = models.BigIntegerField()
    user_address = models.CharField(max_length=100)
    role = models.IntegerField(default=1)  # 1 = User
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'

    def save(self, *args, **kwargs):
        # Password hash only if not already hashed
        if not self.user_password.startswith('pbkdf2_'):
            self.user_password = make_password(self.user_password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.user_password)

    def __str__(self):
        return self.user_name


# =========================
# VAN OPERATOR MODEL
# =========================

class VanOperator(models.Model):

    class OperatorStatus(models.IntegerChoices):
        OFFLINE = 0, 'Offline'
        ONLINE = 1, 'Online'

    class VerificationStatus(models.IntegerChoices):
        NOT_VERIFIED = 0, 'Not Verified'
        VERIFIED = 1, 'Verified'

    operator_id = models.AutoField(primary_key=True)
    operator_name = models.CharField(max_length=30)
    operator_email = models.EmailField(max_length=30, unique=True)
    operator_password = models.CharField(max_length=255)
    operator_phone = models.BigIntegerField()
    operator_license_doc = models.FileField(upload_to='operator_docs/')

    operator_status = models.IntegerField(
        choices=OperatorStatus.choices,
        default=OperatorStatus.OFFLINE
    )

    is_verified = models.IntegerField(
        choices=VerificationStatus.choices,
        default=VerificationStatus.NOT_VERIFIED
    )

    role = models.IntegerField(default=2)  # 2 = Operator
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vanoperator'

    def save(self, *args, **kwargs):
        if not self.operator_password.startswith('pbkdf2_'):
            self.operator_password = make_password(self.operator_password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.operator_password)

    def __str__(self):
        return self.operator_name

# =========================
# USER VEHICLE MODEL
# # =========================
# class UserVehicle(models.Model):
#     vehicle_id = models.AutoField(primary_key=True)
#     user_id = models.IntegerField()
#     vehicle_company = models.CharField(max_length=30)
#     vehicle_name = models.CharField(max_length=30)
#     vehicle_model = models.CharField(max_length=30)
#     vehicle_number = models.CharField(max_length=20,unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)

    

#     class Meta:
#         db_table = 'uservehicle'

#     def __str__(self):
#         return f"{self.vehicle_company} {self.vehicle_name}"

class UserVehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vehicles'
    )

    vehicle_company = models.CharField(max_length=30)
    vehicle_name = models.CharField(max_length=30)
    vehicle_model = models.CharField(max_length=30)
    vehicle_number = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'uservehicle'

    def __str__(self):
        return f"{self.vehicle_company} {self.vehicle_name}"



# =========================
# CHARGING VAN MODEL
# =========================

class ChargingVan(models.Model):
    van_id = models.AutoField(primary_key=True)
    van_number = models.CharField(max_length=15,unique=True)
    operator = models.ForeignKey(
        'VanOperator',  # link to VanOperator model
        on_delete=models.SET_NULL,  # keep van even if operator deleted
        null=True,
        blank=True
    )
    battery_capacity = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chargingvan'

    def __str__(self):
        return self.van_number

# =========================
# REQUEST MODEL
# =========================
class Request(models.Model):

    REQUEST_STATUS = (
        (0,'Pending'),
        (1,'Accepted'),
        (2,'Rejected'),
        (3,'Compeletd')
    )
    request_id = models.AutoField(primary_key=True)
    # user_id = models.IntegerField()
    # operator_id = models.IntegerField()
    # vehicle_id = models.IntegerField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='requests'
    )

    operator = models.ForeignKey(
        VanOperator,
        on_delete=models.CASCADE,
        related_name='operator_requests',
        null=True,
        blank=True
    )

    vehicle = models.ForeignKey(
        UserVehicle,
        on_delete=models.CASCADE,
        related_name='vehicle_requests'
    )
    user_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    user_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    request_status = models.IntegerField(choices=REQUEST_STATUS, default=0)
    # 0=pending, 1=accepted, 2=rejected, 3=completed
    request_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'request'

    def __str__(self):
        return f"Request #{self.request_id}"


# =========================
# BOOKING MODEL
# =========================
class Booking(models.Model):

    BOOKING_STATUS = (
        (0,'In Progress'),
        (1,'Completed')
    )

    booking_id = models.IntegerField(primary_key=True)
    # request_id = models.IntegerField()
    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    # operator_id = models.IntegerField()
    operator = models.ForeignKey(
        VanOperator,
        on_delete=models.CASCADE,
        related_name='operator_booking',
        null=True,
        blank=True
    )
    booking_status = models.IntegerField(default=0,choices=BOOKING_STATUS) # 0=in progress, 1=completed
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'booking'

    def __str__(self):
        return f"{self.booking_id}"
    


# =========================
# PAYMENT MODEL
# =========================
# class Payment(models.Model):
    
#     P_METHOD_STATUS = (
#         (0,'Cash'),
#         (1,'Card'),
#         (2,'UPI'),
#     )
#     P_STATUS = (
#         (0,'Pending'),
#         (1,'Completed')
#     )
    
#     payment_id = models.AutoField(primary_key=True)
#     booking_id = models.IntegerField()
#     user_id = models.IntegerField()
#     operator_id = models.IntegerField()
#     amount = models.FloatField()
#     p_method = models.IntegerField(default=0, choices=P_METHOD_STATUS)
#     # 0=cash, 1=card, 2=upi
#     p_status = models.IntegerField(default=0, choices=P_STATUS)
#     # 0=pending, 1=completed
#     payment_time = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'payment'

#     def __str__(self):
#         return f"Payment #{self.payment_id} - ₹{self.amount}"


class Payment(models.Model):

    P_METHOD_STATUS = (
        (0, 'Cash'),
        (1, 'Card'),
        (2, 'UPI'),
    )

    P_STATUS = (
        (0, 'Pending'),
        (1, 'Completed')
    )

    payment_id = models.AutoField(primary_key=True)

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_payments'
    )

    operator = models.ForeignKey(
        VanOperator,
        on_delete=models.CASCADE,
        related_name='operator_payments'
    )

    amount = models.FloatField()

    p_method = models.IntegerField(
        default=0,
        choices=P_METHOD_STATUS
    )

    p_status = models.IntegerField(
        default=0,
        choices=P_STATUS
    )

    payment_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'payment'

    def __str__(self):
        return f"Payment #{self.payment_id} - ₹{self.amount}"



# =========================
# FEEDBACK MODEL
# =========================
class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
 
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_feedbacks'
    )

    operator = models.ForeignKey(
        VanOperator,
        on_delete=models.CASCADE,
        related_name='operator_feedbacks'
    )
    # user_id = models.IntegerField()
    # operator_id = models.IntegerField()
    rating = models.IntegerField()
    comments = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'feedback'

    def __str__(self):
        return f"Feedback #{self.feedback_id} - {self.rating}⭐"
