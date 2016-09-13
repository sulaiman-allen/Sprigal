from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from api.models import Album, CurrentRfid
# from django.core import serializers
from django.http import HttpResponse
# from api.serializers import AlbumSerializer, CurrentRfidSerializer, PlaylistSerializer
from api.serializers import AlbumSerializer, CurrentRfidSerializer
import os
import json

# Create your views here.


class AlbumList(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    lookup_field = 'rfid'


class RfidList(viewsets.ModelViewSet):
    queryset = CurrentRfid.objects.all()
    serializer_class = CurrentRfidSerializer


def get_directory_list(request):

    playlistList = list()

    path = "/home/xalerons"
    playlistDir = os.path.join(path, 'Playlists')
    os.chdir(playlistDir)
    for file in os.listdir("."):
        playlistList.append(file)

    playlists = {
        "playlists": playlistList
    }

    playlists = json.dumps(playlists)
    return HttpResponse(playlists, content_type="application/json")
