"""
Van Operator views for ChargeNow API.
Operator profile, requests, van management, charging operations.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import VanOperator, ChargingVan, Request, Booking, Payment, Feedback
from ..serializers import (
    VanOperatorSerializer, ChargingVanSerializer, RequestSerializer, 
    BookingSerializer, PaymentSerializer, FeedbackSerializer
)
from ..permissions import IsOperator


class OperatorProfileView(APIView):
    """Get and update operator profile"""
    permission_classes = [IsOperator]
    
    def get(self, request):
        try:
            operator = VanOperator.objects.get(operator_id=request.user['id'])
            serializer = VanOperatorSerializer(operator)
            return Response({'success': True, 'data': serializer.data})
        except VanOperator.DoesNotExist:
            return Response({'success': False, 'message': 'Operator Not Found'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request):
        try:
            operator = VanOperator.objects.get(operator_id=request.user['id'])
            
            if 'operator_name' in request.data:
                operator.operator_name = request.data['operator_name']
            if 'operator_phone' in request.data:
                operator.operator_phone = request.data['operator_phone']            
            if 'operator_email' in request.data:
                operator.operator_email = request.data['operator_email']
            
            operator.save()
            serializer = VanOperatorSerializer(operator)
            return Response({'success': True, 'message': 'Profile Updated', 'data': serializer.data})
        except VanOperator.DoesNotExist:
            return Response({'success': False, 'message': 'Operator Not Found'}, 
                          status=status.HTTP_404_NOT_FOUND)


# ========== STATUS VIEWS ==========

class OperatorStatusView(APIView):
    """Set operator online/offline status"""
    permission_classes = [IsOperator]
    
    def put(self, request):
        try:
            operator = VanOperator.objects.get(operator_id=request.user['id'])
            new_status = request.data.get('status')
            
            if new_status not in [0, 1]:
                return Response({'success': False, 'message': 'Status must be 0 (offline) or 1 (online)'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            operator.operator_status = new_status
            operator.save()
            
            status_text = 'online' if new_status == 1 else 'offline'
            return Response({
                'success': True, 
                'message': f'You are now {status_text}',
                'status': new_status
            })
        except VanOperator.DoesNotExist:
            return Response({'success': False, 'message': 'Operator Not Found'}, 
                          status=status.HTTP_404_NOT_FOUND)


# ========== VAN VIEWS ==========
class OperatorVanView(APIView):
    permission_classes = [IsOperator]

    def get(self, request):
        operator_id = request.user['id']  # int from JWT

        van = ChargingVan.objects.filter(operator_id=operator_id).first()

        if not van:
            return Response(
                {'success': False, 'message': 'No Van Assigned'},
                status=200
            )

        serializer = ChargingVanSerializer(van)
        return Response(
            {'success': True, 'data': serializer.data},
            status=200
        )

# ========== REQUEST VIEWS ==========

class OperatorRequestListView(APIView):
    """View incoming requests"""
    permission_classes = [IsOperator]
    
    def get(self, request):
        requests = Request.objects.filter(operator_id=request.user['id'])
        serializer = RequestSerializer(requests, many=True)
        return Response({'success': True, 'data': serializer.data})


# class OperatorRequestActionView(APIView):
#     """Accept or reject a request"""
#     permission_classes = [IsOperator]
    
#     def put(self, request, request_id):
#         try:
#             req = Request.objects.get(request_id=request_id, operator_id=request.user['id'])
#             action = request.data.get('action')  # 'accept' or 'reject'
            
#             if action == 'accept':
#                 req.request_status = 1  # Accepted
#                 # Create booking
#                 Booking.objects.create(
#                     request_id=req.request_id,
#                     operator_id=request.user['id'],
#                     booking_status=0
#                 )
#                 message = 'Request accepted'
#             elif action == 'reject':
#                 req.request_status = 2  # Rejected
#                 message = 'Request rejected'
#             else:
#                 return Response({'success': False, 'message': 'Action must be accept or reject'}, 
#                               status=status.HTTP_400_BAD_REQUEST)
            
#             req.save()
#             return Response({'success': True, 'message': message})
#         except Request.DoesNotExist:
#             return Response({'success': False, 'message': 'Request not found'}, 
#                           status=status.HTTP_404_NOT_FOUND)

class OperatorRequestActionView(APIView):
    """Accept or reject a request"""
    permission_classes = [IsOperator]
    
    def put(self, request, request_id):
        try:
            ### CHANGE: Retrieve the operator object to pass into Booking creation later
            operator_obj = VanOperator.objects.get(operator_id=request.user['id'])
            
            # Find the specific request assigned to this operator
            req = Request.objects.get(request_id=request_id, operator=operator_obj)
            
            action = request.data.get('action')  # 'accept' or 'reject'
            
            if action == 'accept':
                req.request_status = 1  # Accepted
                
                ### CHANGE: Create booking using Model Instances (req, operator_obj) 
                ### instead of raw IDs. This ensures data integrity.
                Booking.objects.create(
                    request=req,
                    operator=operator_obj,
                    booking_status=0
                )
                message = 'Request Accepted'
            
            elif action == 'reject':
                req.request_status = 2  # Rejected
                message = 'Request Aejected'
            else:
                return Response({'success': False, 'message': 'Action Must Be Accept Or Reject'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            req.save()
            return Response({'success': True, 'message': message})
            
        except Request.DoesNotExist:
            return Response({'success': False, 'message': 'Request not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        except VanOperator.DoesNotExist:
             return Response({'success': False, 'message': 'Operator Profile Error'}, 
                          status=status.HTTP_404_NOT_FOUND)


# ========== CHARGING VIEWS ==========

class OperatorChargingView(APIView):
    """Start Or Complete Charging"""
    permission_classes = [IsOperator]
    
    def put(self, request, booking_id):
        try:
            booking = Booking.objects.get(booking_id=booking_id, operator_id=request.user['id'])
            action = request.data.get('action')  # 'start' or 'complete'
            
            if action == 'start':
                booking.booking_status = 1  # Started
                message = 'Charging Started'
            elif action == 'complete':
                booking.booking_status = 2  # Completed
                # Also mark request as completed
                try:
                    req = Request.objects.get(request_id=booking.request_id)
                    req.request_status = 3  # Completed
                    req.save()
                except Request.DoesNotExist:
                    pass
                message = 'Charging completed'
            else:
                return Response({'success': False, 'message': 'Action must be start or complete'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            booking.save()
            return Response({'success': True, 'message': message})
        except Booking.DoesNotExist:
            return Response({'success': False, 'message': 'Booking not found'}, 
                          status=status.HTTP_404_NOT_FOUND)


# ========== HISTORY VIEWS ==========

# class OperatorBookingHistoryView(APIView):
#     """View booking history"""
#     permission_classes = [IsOperator]
    
#     def get(self, request):
#         bookings = Booking.objects.filter(operator_id=request.user['id'])
#         serializer = BookingSerializer(bookings, many=True)
#         return Response({'success': True, 'data': serializer.data})


class OperatorBookingHistoryView(APIView):
    permission_classes = [IsOperator]

    def get(self, request):
        bookings = Booking.objects.filter(
            operator_id=request.user['id']
        ).select_related(
            'request__user',
            'request__vehicle',
            'operator'
        )

        serializer = BookingSerializer(bookings, many=True)
        return Response({'success': True, 'data': serializer.data})


class OperatorPaymentHistoryView(APIView):
    """View payment history"""
    permission_classes = [IsOperator]
    
    def get(self, request):
        payments = Payment.objects.filter(operator_id=request.user['id'])
        serializer = PaymentSerializer(payments, many=True)
        return Response({'success': True, 'data': serializer.data})


class OperatorFeedbackHistoryView(APIView):
    """View feedback received"""
    permission_classes = [IsOperator]
    
    def get(self, request):
        feedbacks = Feedback.objects.filter(operator_id=request.user['id'])
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response({'success': True, 'data': serializer.data})

# class OperatorFeedbackHistoryView(APIView):
#     """View feedback received"""
#     permission_classes = [IsOperator]
    
#     def get(self, request):
#         # 1. Print the ID from the token
#         current_operator_id = request.user['id']

#         # 2. Check if this operator actually exists
#         operator_exists = VanOperator.objects.filter(operator_id=current_operator_id).exists()

#         # 3. Perform the query
#         feedbacks = Feedback.objects.filter(operator_id=current_operator_id)
        
#         # 5. Serialize
#         serializer = FeedbackSerializer(feedbacks, many=True)
#         return Response({'success': True, 'data': serializer.data})
