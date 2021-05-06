from rest_framework import serializers
from core.models import Trip, TripRequest
from django.contrib.auth import get_user_model

# organizer = models.ForeignKey(
#     settings.AUTH_USER_MODEL,
#     on_delete=models.CASCADE, related_name='organizer'
# )
# start_time = models.DateTimeField()
# end_time = models.DateTimeField()
# additional_info = models.TextField(null=True)
# extra_people = models.ManyToManyField('UserModel', related_name='member')
# start_lat = models.DecimalField(max_digits=9, decimal_places=6)
# start_lon = models.DecimalField(max_digits=9, decimal_places=6)
# end_lat = models.DecimalField(max_digits=9, decimal_places=6)
# end_lon = models.DecimalField(max_digits=9, decimal_places=6)
# start_name = models.CharField(max_length=255)
# dest_name = models.CharField(max_length=255)
# votes = models.IntegerField()


class TripSerializer(serializers.ModelSerializer):
    extra_people = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=get_user_model().objects.all()
    )

    class Meta:
        model = Trip
        fields = ('id', 'start_time', 'end_time', 'additional_info', 'extra_people',
                  'start_lat', 'start_lon', 'end_lat', 'end_lon', 'start_name', 'dest_name', 'voters', 'organizer', 'image')
        read_only_fields = ('id', 'voters', 'organizer', 'image')


class TripRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripRequest
        fields = ('id', 'trip', 'requesters')


class TripImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trip
        fields = ('id', 'image')
        read_only_fields = ('id',)
