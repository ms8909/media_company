from rest_framework import serializers
from .models import Album, SongWriter, Singer, Song


class AlbumSerializer(serializers.ModelSerializer):
    """
    Serializer for Album model.
    """
    class Meta:
        model = Album
        fields = ['title']

class SongWriterSerializer(serializers.ModelSerializer):
    """
    Serializer for SongWriter model.
    """
    class Meta:
        model = SongWriter
        fields = ['name']

class SingerSerializer(serializers.ModelSerializer):
    """
    Serializer for Singer model.
    """
    class Meta:
        model = Singer
        fields = ['name']


class SongSerializer(serializers.ModelSerializer):
    """
    Serializer for Song model. Handles nested serialization for album,
    writers, and singers. Also contains custom create method for handling
    many-to-many relationships.
    """
    album = AlbumSerializer()
    writers = SongWriterSerializer(many=True)
    singers = SingerSerializer(many=True)

    class Meta:
        model = Song
        fields = [
            'id', 'name', 'album', 'writers', 'singers', 'rank',
            'year_released', 'song_time', 'spotify_streams',
            'rolling_stone_ranking', 'nme_ranking', 'ug_views',
            'ug_favourites', 'lyrics'
        ]

    def create(self, validated_data):
        """
        Custom create method for Song model. Manages the creation of related
        Album, SongWriter, and Singer instances.
        """
        writers_data = validated_data.pop('writers', [])
        singers_data = validated_data.pop('singers', [])
        album_data = validated_data.pop('album', None)

        album, _ = Album.objects.get_or_create(**album_data) if album_data else (None, False)
        song = Song.objects.create(**validated_data, album=album)

        for writer_data in writers_data:
            writer, _ = SongWriter.objects.get_or_create(**writer_data)
            song.writers.add(writer)

        for singer_data in singers_data:
            singer, _ = Singer.objects.get_or_create(**singer_data)
            song.singers.add(singer)

        return song


class LimitedSongSerializer(serializers.ModelSerializer):
    """
    Limited serializer for Song model, providing a subset of fields.
    Used for unauthenticated requests.
    """
    album = AlbumSerializer(read_only=True)
    writers = SongWriterSerializer(many=True, read_only=True)

    class Meta:
        model = Song
        fields = ['name', 'album', 'writers', 'rank']