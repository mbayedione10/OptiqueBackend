# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import generics, permissions, status
from api.models import *
from api.serializers import *
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
#login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from django.contrib.auth import authenticate, login

#from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView






def index(request):
    return HttpResponse("Bakeli Team.")


class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    def post (self, request, *args, **kwargs):
            serializer = RegistrationSerializer(data = request.data)
            if not serializer.is_valid():
                return Response({
                    "status": "failure",
                    "message": serializer.errors,
                    "error": "erreur"

                },status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({
                "status": "success",
                "message": "item succesfully created",
                "data": serializer.data,

            }, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    serializer = loginSerializer(data = request.data, many = True)
    email = request.data['email']
    password = request.data['password']

    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=email, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'Token': token.key},
                    status=status.HTTP_200_OK)





class ClientCreateView(generics.CreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    #permission_classes = ()
    serializer_class = ClientSerializer
    def get(self, request, *args, **kwargs):
        client = Client.objects.all()

        if not client:
            return Response({
                "status": "failure",
                "message": "no such item.",
            }, status = status.HTTP_404_NOT_FOUND)

        serializer = ClientSerializer(client, many = True)


        return Response({
            "status": "success",
            "message": "item successfully retrieved.",
            "count": client.count(),
            "data": serializer.data

        },status = status.HTTP_200_OK)



    def post (self, request, *args, **kwargs):
        serializer = ClientSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
                "status": "failure",
                "message": serializer.errors,
                "eroor": "erreur"

            },status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "success",
            "message": "item succesfully created",
            "data": serializer.data

        }, status=status.HTTP_201_CREATED)

class CommandeCreateView(generics.CreateAPIView):
    permission_classes = (
       permissions.IsAuthenticated,
    )
    #permission_classes = ()
    serializer_class = CommandeSerializer
    def get(self, request, *args, **kwargs):
        com = Commande.objects.all()

        if not com:
            return Response({
                "status": "failure",
                "message": "no such item.",
            }, status = status.HTTP_404_NOT_FOUND)

        serializer = CommandeSerializer(com, many = True)

        return Response({
            "status": "success",
            "message": "item successfully retrieved.",
            "count": com.count(),
            "data": serializer.data

        },status = status.HTTP_200_OK)


    @csrf_exempt
    def post (self, request, *args, **kwargs):
        serializer = CommandeSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
                "status": "failure",
                "message": serializer.errors,
                "eroor": "erreur"

            },status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "success",
            "message": "item succesfully created",
            "data": serializer.data

        }, status=status.HTTP_201_CREATED)

class LunetteCreateView(generics.CreateAPIView):
    permission_classes = (
       permissions.IsAuthenticated,
    )
    #permission_classes = ()
    serializer_class = LunetteSerializer
    def get(self, request, *args, **kwargs):
        lunette = Lunette.objects.all()

        if not lunette:
            return Response({
                "status": "failure",
                "message": "no such item.",
            }, status = status.HTTP_404_NOT_FOUND)

        serializer = LunetteSerializer(lunette, many = True)

        return Response({
            "status": "success",
            "message": "item successfully retrieved.",
            "count": lunette.count(),
            "data": serializer.data

        },status = status.HTTP_200_OK)


    @csrf_exempt
    def post (self, request, *args, **kwargs):
        serializer = LunetteSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({
                "status": "failure",
                "message": serializer.errors,
                "eroor": "erreur"

            },status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "success",
            "message": "item succesfully created",
            "data": serializer.data

        }, status=status.HTTP_201_CREATED)
