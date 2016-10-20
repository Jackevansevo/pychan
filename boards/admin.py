from django.contrib import admin
from django.contrib.auth.models import Permission

from .models import Board, Filter, Poster, Reply, Thread


class BoardAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("short_name",)}


class FilterInline(admin.TabularInline):
    model = Filter


class PosterAdmin(admin.ModelAdmin):
    list_display = ('username', 'join_date', 'karma')
    inlines = [
        FilterInline
    ]


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('title', 'bump_count', 'created_on')

# Register your models here.
admin.site.register(Board, BoardAdmin)
admin.site.register(Reply)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Poster, PosterAdmin)
admin.site.register(Permission)
