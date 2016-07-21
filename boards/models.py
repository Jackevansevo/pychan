from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

# Implement thread bump count functionality
# Limit number of POST requests from certain IP Addresses / Sessions
# look at https://github.com/jsocol/django-ratelimit

# Add bots which emulate behaviour of image board, web scraping project, +
# maybe a super simple neural network that attempts to learn an average comment


class Board(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=3)
    slug = AutoSlugField(populate_from='short_name')

    def get_absolute_url(self):
        return reverse('boards:board-detail', args=[self.slug])

    def __str__(self):
        return self.name


class Thread(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=30000)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    board = models.ForeignKey(Board)

    def __str__(self):
        return self.title


class Reply(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    thread = models.ForeignKey(Thread)
    content = models.TextField(max_length=30000)
    image = models.ImageField(upload_to='images/%Y/%m/%d', null=True,
                              blank=True)

    def __str__(self):
        return self.content
