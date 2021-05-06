from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from core.models import UserModel
from google.oauth2 import id_token
from google.auth.transport import requests
from rest_framework import status
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.permissions import AllowAny
from . import serializers

from rest_framework.authtoken.models import Token


# kumar.shubham - c7b6b9a7131fe44591ab03e0a59e06133010983e
# shubhamcrick - 03cd5a4853da5ba25200edada9d72432a290e557


# Create your views here.

# RESPONSE
# {
#  // These six fields are included in all Google ID Tokens.
#  "iss": "https://accounts.google.com",
#  "sub": "110169484474386276334",
#  "azp": "1008719970978-hb24n2dstb40o45d4feuo2ukqmcc6381.apps.googleusercontent.com",
#  "aud": "1008719970978-hb24n2dstb40o45d4feuo2ukqmcc6381.apps.googleusercontent.com",
#  "iat": "1433978353",
#  "exp": "1433981953",
#
#  // These seven fields are only included when the user has granted the "profile" and
#  // "email" OAuth scopes to the application.
#  "email": "testuser@gmail.com",
#  "email_verified": "true",
#  "name" : "Test User",
#  "picture": "https://lh4.googleusercontent.com/-kYgzyAWpZzJ/ABCDEFGHI/AAAJKLMNOP/tIXL9Ir44LE/s99-c/photo.jpg",
#  "given_name": "Test",
#  "family_name": "User",
#  "locale": "en"
# }


class UserLoginView(APIView):
    """auth with google and create or return token"""

    permission_classes = [AllowAny, ]

    CLIENT_ID = ""

    def post(self, request):

        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(
                request.data['id_token'], requests.Request(), audience=None)

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']

            if get_user_model().objects.filter(email=idinfo['email']).exists():
                user = get_user_model().objects.get(email=idinfo['email'])

            else:
                user = get_user_model().objects.create_user(user_name=idinfo['email'],
                                                            email=idinfo['email'], name=idinfo['name'], picture=idinfo['picture'], given_name=idinfo['given_name'], family_name=idinfo['family_name'])
            print(userid)

            token, _ = Token.objects.get_or_create(user=user)
            serializer = serializers.UserSerializer(user)
            return Response({'token': token.key, 'user': serializer.data},
                            status=status.HTTP_200_OK)

            # return Response({'name': idinfo['name'], 'email': idinfo['email']}, status=status.HTTP_200_OK)

        except ValueError:
            # Invalid token
            return Response({'msg': 'token not verified'}, status=status.HTTP_400_BAD_REQUEST)


class UserModelView(APIView):
    permission_classes = [AllowAny, ]

    def get_serializer_class(self):
        if self.action == 'options':
            return serializers.UserAutoCompSer
        return serializers.UserSerializer

    def get_object(self, pk):
        if UserModel.objects.filter(pk=pk).exists():
            return UserModel.objects.get(pk=pk)
        else:
            return None

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        if user:
            serializer = serializers.UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'user does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    def options(self, request, *args, **kwargs):
        q = request.query_params.get("q")
        query = Q(user_name__icontains=q)
        query |= Q(name__icontains=q)
        query |= Q(family_name__icontains=q)
        query_set = UserModel.objects.all().filter(query)

        serializer = serializers.UserAutoCompSer(query_set, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
