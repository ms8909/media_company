from django.urls import path, re_path
from rest_framework import permissions

# Imports for views
from .views import SongList, SongDetail, CSVUploadView, LyricsView

# Imports for swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Songs API",
        default_version='v1',
        description="API for Songs",
        # terms_of_service="URL",
        contact=openapi.Contact(email="contact@songsapi.com"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('songs/', SongList.as_view(), name='song-list'),
    path('songs/<int:pk>/', SongDetail.as_view(), name='Details of a song'),
    path('upload_songs_csv/', CSVUploadView.as_view(), name='Upload songs csv'),
    path('songs/lyrics/<str:song_identifier>/', LyricsView.as_view(), name='song-lyrics'),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
