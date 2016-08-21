from django.contrib import admin
from .models import Board, Reply, Thread, Poster


class BoardAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("short_name",)}


class PosterAdmin(admin.ModelAdmin):
    list_display = ('join_date', 'filters', 'karma')


# Register your models here.
admin.site.register(Board, BoardAdmin)
admin.site.register(Reply)
admin.site.register(Thread)
admin.site.register(Poster, PosterAdmin)
