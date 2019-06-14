from rest_framework import serializers, generics, permissions, status
from api.models import *

from rest_framework import serializers
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.


    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    #token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = CustomUser
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return CustomUser.objects.create_user(**validated_data)

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class LunetteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lunette
        fields = '__all__'

class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class loginSerializer(serializers.ModelSerializer):
    #user = UserSerializer(many=True)

    class Meta:
        model = CustomUser

        fields = ('email', 'password')
