from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.functional import cached_property

# [TODO]
# Order threads by bump count
# Repost timer, prevent save user posting multiple in timeframe
# look at https://github.com/jsocol/django-ratelimit
# Make Celery task to reduce bump count every minute if thread has had no
# replies


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
    bump_limit = models.IntegerField(default=100)
    reply_limit = models.IntegerField(default=5)

    @cached_property
    def get_absolute_url(self):
        return reverse('boards:board-detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class Thread(TimeStampedModel):
    title = models.CharField(max_length=120)
    content = models.TextField(max_length=30000)
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    board = models.ForeignKey(Board, related_name="threads")
    bump_count = models.IntegerField(default=0)
    expired = models.BooleanField(default=False, blank=True)

    @cached_property
    def hit_reply_limit(self):
        # Returns True if Thread has passed it's reply limit
        replies = Reply.objects.filter(thread=self).count()
        if replies > self.board.reply_limit:
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
    thread = models.ForeignKey(Thread, related_name='replies')
    content = models.TextField(max_length=30000)
    image = models.ImageField(upload_to='images/%Y/%m/%d', null=True,
                              blank=True)

    def save(self, *args, **kwargs):
        self.thread.bump_count += 1
        self.thread.save(update_fields=['bump_count'])
        super(Reply, self).save(*args, **kwargs)
        if self.thread.hit_reply_limit:
            self.thread.expired = True
            self.thread.save(update_fields=["expired"])

    def __str__(self):
        return self.content
