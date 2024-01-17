from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

# Swagger related imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import SongSerializer, LimitedSongSerializer
from .models import Song, Album, SongWriter, Singer

# Other imports
import csv
from io import TextIOWrapper
import os
import re



class SongList(generics.ListCreateAPIView):
    # Define the queryset to retrieve songs ordered by their rank
    queryset = Song.objects.all().order_by('rank')
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None # Disable pagination for this view


    def get_serializer_class(self):
        # Return full or limited serializer based on user authentication
        if self.request.user.is_authenticated:
            return SongSerializer
        else:
            return LimitedSongSerializer

    @swagger_auto_schema(request_body=SongSerializer)
    def post(self, request, *args, **kwargs):
        # Allow song creation only for authenticated users
        if self.request.user.is_authenticated:
            return super().post(request, *args, **kwargs)
        else:
            # Return a 401 Unauthorized response for unauthenticated users
            return Response({"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)


class SongDetail(generics.RetrieveAPIView):
    # Set up the view to retrieve a single song
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CSVUploadView(APIView):
    # Specify parsers for handling file upload
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        operation_description="Upload a CSV file",
        manual_parameters=[
            openapi.Parameter(
                name='file',
                in_=openapi.IN_FORM,
                description='CSV file to upload',
                type=openapi.TYPE_FILE,
                required=True
            )
        ],
        responses={status.HTTP_201_CREATED: 'File uploaded successfully'}
    )
    def post(self, request, format=None):
        # Check if there is a file in the request
        if 'file' not in request.data:
            return Response({"message": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the file from request
        file = request.data['file']

        # Process the file
        self.process_csv(file)

        return Response({"message": "File processed successfully"}, status=status.HTTP_201_CREATED)


    def process_csv(self, file):
        """
        Processes a CSV file to create and populate Song, Album, SongWriter, and Singer models.

        Args:
        file: An uploaded file object containing song data.
        """

        # Process the CSV file and create database records
        csv_file = TextIOWrapper(file, encoding='utf-8')
        reader = csv.DictReader(csv_file)

        for row in reader:
            # Create or get the album for each song
            album, _ = Album.objects.get_or_create(title=row['Album'])
            song = Song.objects.create(
                name=row['Song Name'],
                album=album,
                rank=int(row['Rank']),
                year_released=int(row['Year Released']),
                song_time=row['Song Time'],
                spotify_streams=int(row['Spotify Streams'].replace(',', '')),
                rolling_stone_ranking=int(row['Rolling Stone 100 Greatest Beatles Songs Ranking']),
                ug_views=int(row['UG Views']),
                ug_favourites=int(row['UG Favourites'])
            )

            try:
                song.nme_ranking= int(row['NME Top 50 Beatles Songs Ranking'])
            except:
                pass # empty row can not be converted to

            # Process and add writers for the song
            for writer_name in row['Song Writer'].split('\n'):
                writer, _ = SongWriter.objects.get_or_create(name=writer_name.strip())
                song.writers.add(writer)

            # Process and add singers for the song
            for singer_name in row['Singer'].split('\n'):
                singer, _ = Singer.objects.get_or_create(name=singer_name.strip())
                song.singers.add(singer)

            song.save()


class LyricsView(APIView):
    # Restrict this view to authenticated users only
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get lyrics of a song",
        manual_parameters=[
            openapi.Parameter(
                'song_identifier',
                openapi.IN_PATH,
                description="ID or name of the song. Pass a song ID (e.g., '3') or song name (e.g., 'A Hard Day's Night').",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: openapi.Response('Lyrics of the song')}
    )
    def get(self, request, song_identifier, format=None):
        # Try to interpret song_identifier as an ID
        try:
            song_id = int(song_identifier)
            song = Song.objects.get(pk=song_id)
        except (ValueError, Song.DoesNotExist):
            # If not an ID or not found, try to find by name
            song_name = song_identifier.replace('-', ' ').lower()
            song = Song.objects.filter(name__iexact=song_name).first()
            if not song:
                return Response({'detail': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)

        # Fetch and return lyrics
        lyrics = self.get_lyrics(song.name)
        if lyrics is None:
            return Response({'detail': 'Lyrics not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'name': song.name, 'lyrics': lyrics})

    def get_lyrics(self, song_name):
        """
        Retrieves the lyrics for a given song.

        Args:
        song_name (str): The name of the song for which to retrieve lyrics.

        Returns:
        str: The lyrics of the song as a string, or None if the lyrics file is not found.
        """
        # Create a filename from the song name by making it lower case,
        # removing non-alphanumeric characters except spaces, and replacing spaces with hyphens
        sanitized_song_name = re.sub(r'[^\w\s-]', '', song_name.lower()).replace(' ', '-')

        views_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(views_dir, 'object_storage/lyrics', f'{sanitized_song_name}.txt')

        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        return None

