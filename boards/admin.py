from django.contrib import admin
from .models import Thread, Board, Reply

# Register your models here.
admin.site.register(Thread)
admin.site.register(Board)
admin.site.register(Reply)
