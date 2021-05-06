from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView
from . import serializers
from core.models import Trip, UserModel, TripRequest
from django.core.management import call_command
from django.db.models import Count

from math import radians, cos, sin, asin, sqrt

# Create your views here.


class TripViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TripSerializer

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    def get_queryset(self):
        # TODO:move to schedulued job in server
        call_command('expire_trips')
        return Trip.objects.all()

    def get_serializer_class(self):

        # if self.action == 'retrieve':
        #     return serializers.RecipeDetailSerializer

        if self.action == 'upload_image':
            return serializers.TripImageSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        trip = self.get_object()
        serializer = self.get_serializer(
            trip,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class VotesView(APIView):

    def post(self, request):

        trip = Trip.objects.get(pk=request.data['trip_id'])
        user = UserModel.objects.get(pk=request.data['user_id'])

        if not trip or not user:
            return Response({'msg': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)

        if user in trip.voters.all():
            trip.voters.remove(user)
        else:
            trip.voters.add(user)

        fin = serializers.TripSerializer(trip)
        return Response({'trip': fin.data}, status=status.HTTP_200_OK)


class RequestTripView(APIView):
    def get_object(self, pk):
        if Trip.objects.filter(pk=pk).exists():
            return Trip.objects.get(pk=pk)
        else:
            return None

    def get(self, request, pk):
        trip = self.get_object(pk)
        if trip:
            if self.request.user == trip.organizer:
                if TripRequest.objects.filter(trip=trip).exists():
                    tripRequest = TripRequest.objects.get(trip=trip)
                    ser = serializers.TripRequestSerializer(tripRequest)
                    print(TripRequest.requesters)
                    return Response(ser.data, status=status.HTTP_200_OK)
                else:
                    return Response({})
            else:
                return Response({'msg': 'not your trip'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'msg': 'trip does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        trip = self.get_object(pk)
        if trip:
            if self.request.user != trip.organizer:
                tripRequest = None
                if TripRequest.objects.filter(trip=trip).exists():
                    tripRequest = TripRequest.objects.get(trip=trip)
                    tripRequest.requesters.add(self.request.user)
                else:
                    tripRequest = TripRequest(trip=trip)
                    tripRequest.save()
                    tripRequest.requesters.add(self.request.user)
                ser = serializers.TripRequestSerializer(tripRequest)

                return Response(ser.data, status=status.HTTP_200_OK)

            else:
                return Response({'msg': 'can not request in own trip'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': 'no such trip'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        trip = self.get_object(pk)
        if not trip:
            return Response({'msg': 'no such trip'}, status=status.HTTP_400_BAD_REQUEST)
        if self.request.user != trip.organizer:
            return Response({'msg': 'not your trip'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user_id = self.request.data.get("user_id")
            if UserModel.objects.filter(pk=user_id).exists():
                user = UserModel.objects.get(pk=user_id)
                if TripRequest.objects.filter(trip=trip).exists():
                    triprequest = TripRequest.objects.get(trip=trip)
                    if user in triprequest.requesters.all():
                        accept = None
                        accept = self.request.data.get('accept')
                        if accept == "True":
                            trip.extra_people.add(user)
                            triprequest.requesters.remove(user)
                            ser = serializers.TripRequestSerializer(
                                triprequest)
                            return Response(ser.data, status=status.HTTP_200_OK)
                        elif accept == "False":
                            triprequest.requesters.remove(user)
                            ser = serializers.TripRequestSerializer(
                                triprequest)
                            return Response(ser.data, status=status.HTTP_200_OK)
        return Response({'msg': 'invalid request'}, status=status.HTTP_400_BAD_REQUEST)


class PopularTrips(APIView):

    def get(self, request):
        top_trips = Trip.objects.annotate(vote_count=Count('voters')) \
            .order_by('-vote_count')[:7]
        print(top_trips)
        ser = serializers.TripSerializer(top_trips, many=True)
        obj = {"trips": ser.data}
        return Response(obj, status=status.HTTP_200_OK)


class NearTrips(APIView):
    def haversine(self, lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers. Use 3956 for miles
        return c * r

    def get(self, request):
        quer = Trip.objects.all()
        radius = float(self.request.query_params.get('radius'))
        lat = float(self.request.query_params.get('lat'))
        lon = float(self.request.query_params.get('lon'))
        for trip in quer:
            a = self.haversine(getattr(trip, 'start_lon'),
                               getattr(trip, 'start_lat'), lon, lat)
            print(a)
            print(getattr(trip, 'start_lon'))
            print(getattr(trip, 'start_lat'))
            print(radius)
            if a >= radius:
                quer = quer.exclude(id=trip.pk)

        ser = serializers.TripSerializer(quer, many=True)
        obj = {"trips": ser.data}
        return Response(obj, status=status.HTTP_200_OK)
