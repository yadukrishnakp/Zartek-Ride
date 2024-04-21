from django.urls import path, re_path, include
from . import views

urlpatterns = [
    re_path(r'^rides/', include([
        path('create-ride-request', views.CreateOrUpdateRideRequestApiView.as_view()),
        path('get-ride-details-or-list', views.GetRideDetailsOrListApiView.as_view()),
        path('ride-status-change',views.UpdateRideStatusApiView.as_view()),
        path('update-ride-current-location',views.UpdateCurrentRideLocationApiView.as_view()),
        path('update-driver-current-location',views.UpdateCurrentDriverLocationApiView.as_view()),
        path('driver-request-accept', views.UpdateDriverRequestAcceptApiView.as_view()),
    ])),

]