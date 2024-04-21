from django.test import TestCase
from django.urls import reverse
from apps.ride.models import Ride
from apps.users.models import Users
from rest_framework import status
from rest_framework.test import APIClient


class RideRequestApiViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.rider = Users.objects.create(username= "yadu", name= "yadukrishna", email= "yadu@yopmail.com", password= "123",is_active= True,user_type= "Rider")

    def test_create_ride_request(self):

        url = reverse('create-ride-request')
        data = {
            'pickup_latitude':'Your Pickup Latitude',
            'pickup_longitude':'Your Pickup Longitude',
            'dropoff_latitude':'Your Dropoff Latitude',
            'dropoff_longitude':'Your Dropoff Longitude'
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Ride.objects.filter(status='Requested').exists())

    def test_update_ride_request(self):
        ride = Ride.objects.create(rider=self.rider, pickup_latitude='Your Pickup Latitude', pickup_longitude='Your Pickup Longitude', dropoff_latitude='Your Dropoff Latitude', dropoff_longitude='Your Dropoff Longitude', status='Requested')
        url = reverse('create-ride-request', kwargs={'pk': ride.id})
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, 200)
        ride.refresh_from_db()
        self.assertEqual(ride.status, 'Accepted')
