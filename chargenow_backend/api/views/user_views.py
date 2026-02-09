"""
User views for ChargeNow API.
User profile, vehicles, requests, payments, feedback.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models import User, UserVehicle
from ..serializers import (
     UserVehicleSerializer,
)
from ..permissions import IsUser

# VEHICLE VIEWS 

class UserVehicleListView(APIView):
    """Get and add user vehicles"""
    permission_classes = [IsUser]
    
    def get(self, request):
        vehicles = UserVehicle.objects.filter(user_id=request.user['id'])
        serializer = UserVehicleSerializer(vehicles, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user['id']
                
        
        serializer = UserVehicleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True, 
                'message': 'Vehicle added successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVehicleDetailView(APIView):
    """Update and delete user vehicle"""
    permission_classes = [IsUser]
    
    def put(self, request, vehicle_id):
        try:
            vehicle = UserVehicle.objects.get(vehicle_id=vehicle_id, user_id=request.user['id'])
            
            if 'vehicle_company' in request.data:
                vehicle.vehicle_company = request.data['vehicle_company']
            if 'vehicle_name' in request.data:
                vehicle.vehicle_name = request.data['vehicle_name']
            if 'vehicle_model' in request.data:
                vehicle.vehicle_model = request.data['vehicle_model']
            if 'vehicle_number' in request.data:
                vehicle.vehicle_number = request.data['vehicle_number']
            
            vehicle.save()
            serializer = UserVehicleSerializer(vehicle)
            return Response({'success': True, 'message': 'Vehicle updated', 'data': serializer.data})
        except UserVehicle.DoesNotExist:
            return Response({'success': False, 'message': 'Vehicle not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, vehicle_id):
        try:
            vehicle = UserVehicle.objects.get(vehicle_id=vehicle_id, user_id=request.user['id'])
            vehicle.delete()
            return Response({'success': True, 'message': 'Vehicle deleted successfully'})
        except UserVehicle.DoesNotExist:
            return Response({'success': False, 'message': 'Vehicle not found'}, 
                          status=status.HTTP_404_NOT_FOUND)


