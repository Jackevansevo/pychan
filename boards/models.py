from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

# Save User Filters in DB, also have filters tied to a session
# Implement thread bump count functionality
# Limit number of POST requests from certain IP Addresses / Sessions
# look at https://github.com/jsocol/django-ratelimit

# Add bots which emulate behaviour of image board, web scraping project, +
# maybe a super simple neural network that attempts to learn an average comment


class TimeStampedModel(models.Model):
    """Adds created_on, and modified_on Fields to all subclasses"""
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Filter(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Board(models.Model):
    name = models.CharField(max_length=15)
    short_name = models.CharField(max_length=3)
    slug = AutoSlugField(populate_from='short_name')

    def get_absolute_url(self):
        return reverse('boards:board-detail', args=[self.slug])

    def __str__(self):
        return self.name


class Thread(TimeStampedModel):
    title = models.CharField(max_length=120)
    content = models.TextField(max_length=30000)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    board = models.ForeignKey(Board)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Reply(models.Model):
    replies = models.ManyToManyField("self", blank=True)
    user = models.ForeignKey(User, blank=True, null=True)
    thread = models.ForeignKey(Thread)
    content = models.TextField(max_length=30000)
    image = models.ImageField(upload_to='images/%Y/%m/%d', null=True,
                              blank=True)

    def __str__(self):
        return self.content
