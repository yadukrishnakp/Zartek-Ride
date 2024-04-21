from apps.ride.models import Ride
from apps.user.models import Users
from rest_framework import serializers
from rides_core.helpers.helper import  find_driver, get_object_or_none

class CreateOrUpdateRidesSerializer(serializers.Serializer):
    id                = serializers.IntegerField(required=False,allow_null=True)
    pickup_latitude   = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    pickup_longitude  = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    dropoff_latitude  = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)
    dropoff_longitude = serializers.CharField(max_length=250, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model   = Ride
        fields = ['id','pickup_latitude', 'pickup_longitude','dropoff_latitude','dropoff_longitude']

    def validate(self, attrs):
        return super().validate(attrs)
    

    def create(self, validated_data):
        pickup_latitude   = validated_data.get('pickup_latitude', None)
        pickup_longitude  = validated_data.get('pickup_longitude', None)
        request           = self.context.get('request',None)
        instance                    = Ride()
        instance.rider_id           = request.user.id
        instance.pickup_latitude    = pickup_latitude
        instance.pickup_longitude   = pickup_longitude
        instance.dropoff_latitude   = validated_data.get('dropoff_latitude', None)
        instance.dropoff_longitude  = validated_data.get('dropoff_longitude', None)
        instance.save()
        instance.status             = 'Requested'
        
        closest_driver, shortest_distance = find_driver(request,instance)
        instance.driver = closest_driver
        instance.distance_to_rider = shortest_distance
        instance.save()
        
        return instance

    def update(self, instance, validated_data):
        pickup_latitude   = validated_data.get('pickup_latitude', None)
        pickup_longitude  = validated_data.get('pickup_longitude', None)
        request         = self.context.get('request',None)
        
        instance.rider_id           = request.user.id
        instance.pickup_latitude    = pickup_latitude
        instance.pickup_longitude   = pickup_longitude
        instance.dropoff_latitude   = validated_data.get('dropoff_latitude', None)
        instance.dropoff_longitude  = validated_data.get('dropoff_longitude', None)
        instance.save()
        closest_driver, shortest_distance = find_driver(request,instance)
        instance.driver = closest_driver
        instance.distance_to_rider = shortest_distance
        
        return instance
    


class RideStatusChangeSerializer(serializers.Serializer):
    id        = serializers.IntegerField(required=True,allow_null=True)
    status    = serializers.ChoiceField(choices=Ride.StatusChoice.choices, required=False, allow_null=True, allow_blank=True)
    
    class Meta:
        model   = Ride
        fields = ['id','status']

    def validate(self, attrs):
        return super().validate(attrs)

    def update(self, instance, validated_data):
        request         = self.context.get('request',None)
        status = validated_data.get('status', None)
        if instance.driver not in ['', None]:
            user_obj = get_object_or_none(Users, pk=instance.driver.id)
            if status in ['InTravel', 'Started', 'Accepted']:
                user_obj = get_object_or_none(Users, pk=instance.driver.id)
                user_obj.is_completed = False
            else:
                user_obj.is_completed = True
            user_obj.save()

        instance.status = validated_data.get('status', None)

        instance.save()
        return instance
    

class RideUpdateCurrentLocationSerializer(serializers.Serializer):
    id        = serializers.IntegerField(required=True,allow_null=True)
    latitude  = serializers.CharField(required=True)
    longitude = serializers.CharField(required=True)

    class Meta:
        model   = Ride
        fields = ['id', 'latitude', 'longitude']

    def validate(self, attrs):
        return super().validate(attrs)

    def update(self, instance, validated_data):
        request         = self.context.get('request',None)
        instance.current_latitude = validated_data.get('latitude', None)
        instance.current_longitude = validated_data.get('longitude', None)
        instance.save()
        return instance
    

class UpdateCurrentDriverLocationSerializer(serializers.ModelSerializer):
    id         = serializers.IntegerField(required=False,allow_null=True)
    latitude   = serializers.CharField(required=True)
    longitude  = serializers.CharField(required=True)
  
    class Meta:
        model = Users 
        fields = ['id','latitude','longitude']
    
    
    def validate(self, attrs):
        return super().validate(attrs)

    
    def update(self, instance, validated_data):
        instance.latitude    = validated_data.get('latitude')
        instance.longitude   = validated_data.get('longitude')
        instance.save()
        return instance
    

class RideAcceptRequestSerializer(serializers.Serializer):
    id        = serializers.IntegerField(required=True,allow_null=True)
    status    = serializers.ChoiceField(choices=Ride.StatusChoice.choices, required=False, allow_null=True, allow_blank=True)
    
    class Meta:
        model   = Ride
        fields = ['id','status']

    def validate(self, attrs):
        return super().validate(attrs)

    def update(self, instance, validated_data):
        request         = self.context.get('request',None)
        status          = validated_data.get('status', None)
        if instance.driver not in ['', None]:
            user_obj = get_object_or_none(Users, pk=instance.driver.id)
            if status in ['InTravel', 'Started', 'Accepted']:
                user_obj = get_object_or_none(Users, pk=instance.driver.id)
                user_obj.is_completed = False
            else:
                user_obj.is_completed = True
            user_obj.save()

        instance.status = validated_data.get('status', None)

        instance.save()
        return instance