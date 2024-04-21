from django.shortcuts import render
from apps.ride.models import Ride
from apps.ride.schemas import RideDetailsOrListingSchema
from apps.ride.serializers import CreateOrUpdateRidesSerializer, RideAcceptRequestSerializer, RideStatusChangeSerializer, RideUpdateCurrentLocationSerializer, UpdateCurrentDriverLocationSerializer
from apps.user.models import Users
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rides_core.helpers.helper import get_object_or_none
from rides_core.helpers.pagination import RestPagination
from rides_core.helpers.response import ResponseInfo
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
import sys, os
from django.db.models import Q
from rides_core.helpers.custom_messages import _success,_record_not_found

# Create your views here.



class CreateOrUpdateRideRequestApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateRideRequestApiView, self).__init__(**kwargs)
    
    serializer_class          = CreateOrUpdateRidesSerializer
    permission_classes        = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Ride"])
    def post(self, request):
        try:
            
            instance = get_object_or_none(Ride,pk=request.data.get('id',None))

            serializer = self.serializer_class(instance, data=request.data, context = {'request' : request})
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()

            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
                
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class GetRideDetailsOrListApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetRideDetailsOrListApiView, self).__init__(**kwargs)
    
    serializer_class    = RideDetailsOrListingSchema
    permission_classes  = [IsAuthenticated]
    pagination_class    = RestPagination
  
    id        = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Enter The Id ", required=False)
  
    @swagger_auto_schema(tags=["Ride"], manual_parameters=[id], pagination_class=RestPagination)
    def get(self, request):
        
        try:
            id    = request.GET.get('id', None)

            filter_set = Q()
            if id not in ['',None]:
                filter_set = Q(id=id)
     
            queryset    = Ride.objects.filter(filter_set).order_by('-id')
            page        = self.paginate_queryset(queryset)
            serializer  = self.serializer_class(page, many=True,context={'request':request})
            return self.get_paginated_response(serializer.data)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


class UpdateRideStatusApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UpdateRideStatusApiView, self).__init__(**kwargs)
    
    serializer_class          = RideStatusChangeSerializer
    permission_classes        = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Ride"])
    def post(self, request):
        try:
            
            instance = get_object_or_none(Ride, pk=request.data.get('id',None))

            serializer = self.serializer_class(instance, data=request.data, context = {'request' : request})
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()

            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
                
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateCurrentRideLocationApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UpdateCurrentRideLocationApiView, self).__init__(**kwargs)
    
    serializer_class          = RideUpdateCurrentLocationSerializer
    permission_classes        = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Ride"])
    def post(self, request):
        try:
            
            instance = get_object_or_none(Ride, pk=request.data.get('id',None))

            serializer = self.serializer_class(instance, data=request.data, context = {'request' : request})
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()

            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
                
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateCurrentDriverLocationApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UpdateCurrentDriverLocationApiView, self).__init__(**kwargs)
        
    serializer_class   = UpdateCurrentDriverLocationSerializer
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Ride"])
    def post(self, request):
        try:

            user_instance = get_object_or_none(Users, pk=request.data.get('id',None))
           
            serializer = self.serializer_class(user_instance, data=request.data, context = {'request' : request})
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateDriverRequestAcceptApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UpdateDriverRequestAcceptApiView, self).__init__(**kwargs)
    
    serializer_class          = RideAcceptRequestSerializer
    permission_classes        = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Ride"])
    def post(self, request):
        try:
            
            instance = get_object_or_none(Ride, pk=request.data.get('id',None))

            serializer = self.serializer_class(instance, data=request.data, context = {'request' : request})
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()

            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
                
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
