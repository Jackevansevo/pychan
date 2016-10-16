from django.contrib import admin
from .models import Board, Reply, Thread, Poster


class BoardAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("short_name",)}


class PosterAdmin(admin.ModelAdmin):
    list_display = ('username', 'join_date', 'filters', 'karma')


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'bump_count', 'created_on')

# Register your models here.
admin.site.register(Board, BoardAdmin)
admin.site.register(Reply)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Poster, PosterAdmin)
