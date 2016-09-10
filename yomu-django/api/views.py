from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from api.models import Album, CurrentRfid
from api.serializers import AlbumSerializer, CurrentRfidSerializer

# Create your views here.

class AlbumList(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    lookup_field = 'rfid'

class RfidList(viewsets.ModelViewSet):
	queryset = CurrentRfid.objects.all()
	serializer_class = CurrentRfidSerializer