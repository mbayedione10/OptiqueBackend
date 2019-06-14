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


#information de l'utilisateur qui a fait la commande
class UserByCommandeView(generics.ListAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    #permission_classes = ()
    userSet = CustomUser.objects.all()
    serializer_class = UserSerializer
    def get(self, request, *args, **kwargs):
        user = CustomUser.objects.filter(commande = kwargs['pk'])

        if not user:
            return Response({
                "status": "failure",
                "message": "no such item.",
            }, status = status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, many = True)

        return Response({
            "status": "success",
            "message": "item successfully retrieved.",
            "count": user.count(),
            "data": serializer.data

        },status = status.HTTP_200_OK)



#ajouter des clients  et les lister
class ClientCreateView(generics.CreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    #permission_classes = ()
    serializer_class = ClientSerializer
    #liste des clients
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


    #enregistrer un client
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

#modifier un client
class ClientUpdateView(generics.CreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    #permission_classes = ()
    serializer_class = ClientSerializer
    def put (self, request, *args, **kwargs):
        try:
            #recuperer l'id du client
            client = Client.objects.get(id= kwargs['pk'])
        except Client.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        client_data = {
            'firstname': request.data['firstname'],
            'lastname': request.data['lastname'],
            'phone': request.data['phone'],
            'photo': request.data['photo'],
            'adress': request.data['adress'],
        }
        #inserer les modifications
        serializer = ClientSerializer(client, data = client_data, partial = True)

        if not serializer.is_valid():
            return Response({
                    "status": "failure",
                    "message": "invalid data",
                    "eroors": serializer.errors

            },status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "success",
            "message": "item successfully update.",
            "data": serializer.data

        },status = status.HTTP_200_OK)

#supprimer un client
class ClientDeleteView(generics.CreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    #permission_classes = ()
    serializer_class = ClientSerializer
    def get (self, request, *args, **kwargs):
        try:
            #recuperer l'id du client
            client = Client.objects.get(id = kwargs['pk'])
        except Client.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        client.delete()
        return Response({
            "status": "success",
            "message": "item successfully deleted."

        },status = status.HTTP_200_OK)

#retrouver le client a partir de son id
class ClientByIdView(generics.ListAPIView):
    #Autorisation si la personne est connectée
    permission_classes = (
        permissions.IsAuthenticated,
    )
    #permission_classes = ()
    ClientSet = Client.objects.all()
    serializer_class = ClientSerializer
    def get(self, request, *args, **kwargs):
        client =Client.objects.filter(id = kwargs['pk'])

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


#information du client d'une commande
class ClientByCommandeView(generics.ListAPIView):
    #permission_classes = (
    #    permissions.IsAuthenticated,
    #)
    permission_classes = ()
    ClientSet = Client.objects.all()
    serializer_class = ClientSerializer
    def get(self, request, *args, **kwargs):
        client = Client.objects.filter(commande = kwargs['pk'])

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



#ajouter une commande
class CommandeCreateView(generics.CreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    #permission_classes = ()
    serializer_class = CommandeSerializer
    #liste des commandes
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

    #ajouter une commande
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

#modifier une commande
class CommandeUpdateView(generics.CreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    #permission_classes = ()
    serializer_class = CommandeSerializer
    def put (self, request, *args, **kwargs):
        try:
            #recuperer l'id de la commande
            com = Commande.objects.get(id= kwargs['pk'])
        except Commande.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        commande_data = {
            'client': request.data['client'],
            'user': request.data['user'],
            'lunette': request.data['lunette'],
            'date': request.data['date'],
            'nbre_lunettes': request.data['nbre_lunettes'],
            'montant_total': request.data['montant_total'],
        }
        #enregistrer les commandes
        serializer = CommandeSerializer(com, data = commande_data, partial = True)

        if not serializer.is_valid():
            return Response({
                    "status": "failure",
                    "message": "invalid data",
                    "eroors": serializer.errors

            },status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "success",
            "message": "item successfully update.",
            "data": serializer.data

        },status = status.HTTP_200_OK)

#supprimer une commande a partir de l'id
class CommandeDeleteView(generics.CreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    #permission_classes = ()
    permission_classes = ()
    serializer_class = CommandeSerializer
    def get (self, request, *args, **kwargs):
        try:
            commande = Commande.objects.get(id = kwargs['pk'])
        except Commande.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        commande.delete()
        return Response({
            "status": "success",
            "message": "item successfully deleted."

        },status = status.HTTP_200_OK)


#retrouver la commande a partir de son id
class CommandeByIdView(generics.ListAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    #permission_classes = ()
    commandeSet = Commande.objects.all()
    serializer_class = CommandeSerializer
    def get(self, request, *args, **kwargs):
        commande =Commande.objects.filter(id = kwargs['pk'])

        if not commande:
            return Response({
                "status": "failure",
                "message": "no such item.",
            }, status = status.HTTP_404_NOT_FOUND)

        serializer = CommandeSerializer(commande, many = True)

        return Response({
            "status": "success",
            "message": "item successfully retrieved.",
            "count": commande.count(),
            "data": serializer.data

                },status = status.HTTP_200_OK)




class LunetteCreateView(generics.CreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    #permission_classes = ()
    serializer_class = LunetteSerializer
    #liste des lunettes
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

    #ajouter une lunette
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

#mettre a jour les informations d'une lunette
class LunetteUpdateView(generics.CreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    #permission_classes = ()
    serializer_class = LunetteSerializer
    def put (self, request, *args, **kwargs):
        try:
            lunette = Lunette.objects.get(id= kwargs['pk'])
        except Lunette.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        lunette_data = {
            'name': request.data['name'],
            'type': request.data['type'],
            'price': request.data['price'],
            'photo': request.data['photo'],
        }

        serializer = LunetteSerializer(lunette, data = lunette_data, partial = True)

        if not serializer.is_valid():
            return Response({
                    "status": "failure",
                    "message": "invalid data",
                    "eroors": serializer.errors

            },status = status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({
            "status": "success",
            "message": "item successfully update.",
            "data": serializer.data

        },status = status.HTTP_200_OK)

#supprimer une lunette a partir de l'id
class LunetteDeleteView(generics.CreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    #permission_classes = ()
    serializer_class = LunetteSerializer
    def get (self, request, *args, **kwargs):
        try:
            lunette = Lunette.objects.get(id = kwargs['pk'])
        except Lunette.DoesNotExist:
            return Response({
                "status": "failure",
                "message": "no such item"
            }, status=status.HTTP_400_BAD_REQUEST)

        lunette.delete()
        return Response({
            "status": "success",
            "message": "item successfully deleted."

        },status = status.HTTP_200_OK)

#retrouver la lunette a partir de son id
class LunetteByIdView(generics.ListAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    #permission_classes = ()
    lunetteSet = Lunette.objects.all()
    serializer_class = LunetteSerializer
    def get(self, request, *args, **kwargs):
        lunette =Lunette.objects.filter(id = kwargs['pk'])

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

#information de la lunette d'une commande
class LunetteByCommandeView(generics.ListAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    #permission_classes = ()
    lunette = Lunette.objects.all()
    serializer_class = LunetteSerializer
    def get(self, request, *args, **kwargs):
        lunette = Lunette.objects.filter(commande = kwargs['pk'])

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
