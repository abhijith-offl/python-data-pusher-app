from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Data Pusher application!")


# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
import requests

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

class DataHandlerViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='incoming_data')
    def handle_data(self, request):
        app_secret_token = request.headers.get('CL-X-TOKEN')
        if not app_secret_token:
            return Response({"message": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED)
        
        account = get_object_or_404(Account, app_secret_token=app_secret_token)
        
        data = request.data
        if not isinstance(data, dict):
            return Response({"message": "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)
        
        for destination in account.destinations.all():
            headers = destination.headers
            if destination.http_method == 'GET':
                response = requests.get(destination.url, headers=headers, params=data)
            elif destination.http_method == 'POST':
                response = requests.post(destination.url, headers=headers, json=data)
            elif destination.http_method == 'PUT':
                response = requests.put(destination.url, headers=headers, json=data)
        
        return Response({"message": "Data sent successfully"}, status=status.HTTP_200_OK)
