from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.functional import cached_property

# [TODO]
# Order threads by bump count
# Prevent submitting images to threads that have 404'd
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

    @cached_property
    def get_absolute_url(self):
        return reverse('boards:board-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Thread(TimeStampedModel):
    title = models.CharField(max_length=120)
    content = models.TextField(max_length=30000)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    board = models.ForeignKey(Board)

    class Meta:
        # [TODO] Order by bump count
        ordering = ['-created_on']

    @cached_property
    def bump_count(self):
        # Returns the bump count of the Thread, placeholder for now
        pass

    @cached_property
    def hit_reply_limit(self):
        # Returns True if Thread has passed it's reply limit
        replies = Reply.objects.all().filter(thread=self).count()
        if replies > 5:
            return True
        return False

    @cached_property
    def is_active(self):
        # Returns True if Thread has had a reply in the last 5 minutes
        latest_reply = Reply.objects.all().filter(thread=self).last()
        return latest_reply.created_on

    @cached_property
    def has_404d(self):
        # Returns True if Thread has 404'd
        if self.hit_reply_limit:
            return True
        return False

    @cached_property
    def get_absolute_url(self):
        return reverse('boards:thread-detail', kwargs={'slug': self.board.slug,
                                                       'pk': self.id})

    def __str__(self):
        return self.title


class Reply(TimeStampedModel):
    replies = models.ManyToManyField("self", blank=True)
    user = models.ForeignKey(User, blank=True, null=True)
    thread = models.ForeignKey(Thread)
    content = models.TextField(max_length=30000)
    image = models.ImageField(upload_to='images/%Y/%m/%d', null=True,
                              blank=True)

    def __str__(self):
        return self.content
