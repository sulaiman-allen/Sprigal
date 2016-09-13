from django.db import models

# Create your models here.


class Album(models.Model):
    title = models.CharField(max_length=60)
    artist = models.CharField(max_length=60)
    playlist = models.CharField(max_length=200)
    rfid = models.CharField(max_length=10, null=True)

    def __str__(self):
        return "{}: {}".format(self.rfid, self.title)

    def __unicode__(self):
        return "{}: {}".format(self.rfid, self.title)


class CurrentRfid(models.Model):
    rfid = models.CharField(max_length=10, null=True)

    def __str__(self):
        return "{}: {}".format(self.id, self.rfid)

    def __unicode__(self):
        return "{}: {}".format(self.id, self.rfid)


# class PlaylistList(models.Model):
#     playlists = models.CharField(max_length=2000, null=True)

#     def __str__(self):
#         return "{}: {}".format(self.id, self.playlists)

#     def __unicode__(self):
#         return "{}: {}".format(self.id, self.playlists)