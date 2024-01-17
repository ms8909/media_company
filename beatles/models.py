from django.db import models

# Create your models here.

class Album(models.Model):
    """
    Represents a music album.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class SongWriter(models.Model):
    """
    Represents an individual who writes songs.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Singer(models.Model):
    """
    Represents a singer or vocalist.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Song(models.Model):
    """
    Represents a song with associated details like album, writers, and singers.

    Fields:
    name (CharField): The name of the song.
    album (ForeignKey): The album to which this song belongs.
    writers (ManyToManyField): The songwriters of the song.
    singers (ManyToManyField): The singers or vocalists of the song.
    rank (IntegerField): The rank or position of the song.
    year_released (IntegerField): The release year of the song.
    song_time (CharField): Duration of the song.
    spotify_streams (IntegerField): Number of streams on Spotify.
    rolling_stone_ranking (IntegerField): Ranking on Rolling Stone's list.
    nme_ranking (IntegerField): Ranking on NME's list, nullable.
    ug_views (IntegerField): Number of views on Ultimate Guitar.
    ug_favourites (IntegerField): Number of times favorited on Ultimate Guitar.
    lyrics (JSONField): The lyrics of the song, stored in JSON format.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    writers = models.ManyToManyField(SongWriter)
    singers = models.ManyToManyField(Singer)
    rank = models.IntegerField()
    year_released = models.IntegerField()
    song_time = models.CharField(max_length=10)  # Example: '02:32'
    spotify_streams = models.IntegerField()
    rolling_stone_ranking = models.IntegerField()
    nme_ranking = models.IntegerField(null=True, blank=True)  # Some songs might not have this ranking
    ug_views = models.IntegerField()
    ug_favourites = models.IntegerField()
    lyrics = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['id']),
            models.Index(fields=['rank']),
            models.Index(fields=['year_released']),
        ]


