from apps.ride.models import Ride
from apps.user.models import Users
from rest_framework import serializers


class GetUserResponseSchemas(serializers.ModelSerializer):    
    class Meta:
        model  = Users
        fields = ['id', 'name', 'email', 'username', 'is_active', 'latitude', 'longitude']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas


class RideDetailsOrListingSchema(serializers.ModelSerializer):
    rider  = serializers.SerializerMethodField('get_rider')
    driver = serializers.SerializerMethodField('get_driver')

    class Meta:
        model = Ride
        fields = ['id','rider', 'driver','pickup_latitude','pickup_longitude', 'dropoff_latitude', 'dropoff_longitude','status', 'created_at', 'updated_at',]
    
    def get_rider(self, instance):
        request = self.context.get('request')
        user_obj = Users.objects.filter(id=instance.rider.id)
        user_schema = GetUserResponseSchemas(user_obj, many=True,context={"request": request})
        return user_schema.data
    
    def get_driver(self, instance):
        request = self.context.get('request')
        if instance.driver not in ['', None]:
            user_obj = Users.objects.filter(id=instance.driver.id)
            user_schema = GetUserResponseSchemas(user_obj, many=True,context={"request": request})
            return user_schema.data
        return ''
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas