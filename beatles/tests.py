from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Song, Album, Singer, SongWriter
import os
import json

class SongAPITestCase(APITestCase):

    def setUp(self):
        # Create a user and anbum, writers and singers for testing
        self.user = User.objects.create(username= 'evident')
        self.user.set_password('dev_interview')
        self.user.save()

        self.album = Album.objects.create(title='Test Album')
        self.writer1 = SongWriter.objects.create(name='John Doe')
        self.writer2 = SongWriter.objects.create(name='Jane Smith')
        self.singer1 = Singer.objects.create(name='Alice Cooper')
        self.singer2 = Singer.objects.create(name='Freddie Mercury')

        self.lyrics_file = 'test-song.txt'
        self.lyrics_content = "Sample lyrics for testing."

        # Create a dummy lyrics file
        views_dir = os.path.dirname(os.path.abspath(__file__))
        self.filepath = os.path.join(views_dir, 'object_storage/lyrics', self.lyrics_file)
        with open(self.filepath, 'w', encoding='utf-8') as file:
            file.write(self.lyrics_content)

        # Create a song
        self.song = Song.objects.create(
            name='Test Song',
            album=self.album,
            rank=1,
            year_released=2020,
            song_time='03:30',
            spotify_streams=100000,
            rolling_stone_ranking=2,
            ug_views=5000,
            ug_favourites=300,
            # If you have a lyrics field in your Song model, you can set it here as well
        )

        # Add the songwriters and singers to the song
        self.song.writers.add(self.writer1)
        self.song.singers.add(self.singer1)


    def test_song_list_authenticated(self):
        # Authenticate the user
        login_successful = self.client.login(username='evident', password='dev_interview')

        # Get the response from the song list API
        response = self.client.get(reverse('song-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_song_list_unauthenticated(self):
        # Get the response from the song list API without authentication
        response = self.client.get(reverse('song-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_song_create_authenticated(self):
        # Authenticate the user
        login_successful = self.client.login(username='evident', password='dev_interview')

        # Data for creating a song, including necessary fields and relationships
        data = {
            'name': 'New Song',
            'album': {'title': 'Test Album'},
            'rank': 1,
            'year_released': 2021,
            'song_time': '03:30',
            'spotify_streams': 100000,
            'rolling_stone_ranking': 5,
            'ug_views': 1500,
            'ug_favourites': 100,
            'nme_ranking': 100,
            'writers': [{'name': self.writer1.name}, {'name': self.writer2.name}],
            'singers': [{'name': self.singer1.name}, {'name': self.singer2.name}],
            'lyrics': json.dumps({'lyrics_text': "These are the lyrics of the song."}),
        }

        # Post request to create a new song
        response = self.client.post(reverse('song-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_song_create_unauthenticated(self):
        # Data for creating a song
        data = {
            'name': 'New Song',
            'album': {'title': 'Test Album'},
            'rank': 1,
            'year_released': 2021,
            'song_time': '03:30',
            'spotify_streams': 100000,
            'rolling_stone_ranking': 5,
            'ug_views': 1500,
            'ug_favourites': 100,
            'nme_ranking': 100,
            'writers': [{'name': self.writer1.name}, {'name': self.writer2.name}],
            'singers': [{'name': self.singer1.name}, {'name': self.singer2.name}],
            'lyrics': json.dumps({'lyrics_text': "These are the lyrics of the song."}),
        }

        # Attempt to create a new song without authentication
        response = self.client.post(reverse('song-list'), data, format='json')

        # The API should return a 401 Unauthorized status code
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        # Clean up the dummy lyrics file after tests
        os.remove(self.filepath)

    def test_get_lyrics_authenticated(self):
        # Authenticate the user
        login_successful = self.client.login(username='evident', password='dev_interview')
        print(login_successful)

        # Request the lyrics for the created song
        url = reverse('song-lyrics', args=[self.song.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['lyrics'], self.lyrics_content)


    def test_get_lyrics_unauthenticated(self):
        # Request lyrics without authentication
        url = reverse('song-lyrics', args=[self.song.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_lyrics_song_not_found(self):
        # Authenticate the user
        login_successful = self.client.login(username='evident', password='dev_interview')
        print(login_successful)

        # Request lyrics for a non-existent song
        url = reverse('song-lyrics', args=['non existent song sssss'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



