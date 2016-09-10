from rest_framework import serializers
from api.models import Album, CurrentRfid

class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    '''
        Returns a json of the values associated with an rfid tag.
    '''

    class Meta:
        model = Album
        fields = ('id', 'url', 'title', 'artist', 'playlist', 'rfid')

        lookup_field = 'rfid'
        extra_kwargs = {
            'url': {'lookup_field': 'rfid'}
        }

class CurrentRfidSerializer(serializers.HyperlinkedModelSerializer):
    '''
        Serializer for sending the current rfid value to a an angularJs client for prefilling a 
        web form based upon last scanned item that wasn't found in the database.
    '''

    class Meta:
        model = CurrentRfid
        fields = ('id', 'url', 'rfid')
