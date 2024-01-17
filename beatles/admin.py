from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Album, Song, SongWriter, Singer

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(SongWriter)
admin.site.register(Singer)