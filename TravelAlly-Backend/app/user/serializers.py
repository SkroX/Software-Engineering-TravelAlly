from rest_framework import serializers
from core.models import UserModel
from django.contrib.auth import get_user_model

# email = models.EmailField(max_length=255, unique=True)
# name = models.CharField(max_length=255)
# picture = models.URLField(default=None, blank=True, null=True)
# given_name = models.CharField(max_length=255)
# family_name = models.CharField(max_length=255, blank=True)
#
# is_active = models.BooleanField(default=True)
# is_staff = models.BooleanField(default=False)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()

        fields = ('id', 'email', 'name', 'picture', 'given_name',
                  'family_name', 'is_staff', 'is_active')
        read_only_fields = ('id',)


class UserAutoCompSer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()

        fields = ('id', 'name', 'picture', 'family_name', )
