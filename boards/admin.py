from django.contrib import admin
from .models import Board, Filter, Reply, Thread

# Register your models here.
admin.site.register(Board)
admin.site.register(Filter)
admin.site.register(Reply)
admin.site.register(Thread)
