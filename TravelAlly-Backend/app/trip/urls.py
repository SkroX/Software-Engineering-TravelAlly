from django.urls import path, include
from rest_framework.routers import DefaultRouter

from trip import views

router = DefaultRouter()
router.register('trips', views.TripViewSet, basename='trips')

app_name = 'trip'

urlpatterns = [
    path('', include(router.urls)),
    path('vote/', views.VotesView.as_view(), name='vote'),
    path('request/<int:pk>/', views.RequestTripView.as_view(), name='request'),
    path('popular/', views.PopularTrips.as_view(), name='popular'),
    path('nearme/', views.NearTrips.as_view(), name='near')
]
