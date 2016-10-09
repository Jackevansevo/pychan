from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.text import slugify

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


class Poster(AbstractUser):
    join_date = models.DateTimeField(auto_now_add=True)
    filters = ArrayField(
        models.CharField(max_length=200),
        blank=True,
        default=[]
    )
    karma = models.PositiveIntegerField(default=0, blank=True)


class Board(models.Model):
    name = models.CharField(max_length=15)
    short_name = models.CharField(max_length=3)
    slug = models.SlugField(unique=True)
    bump_limit = models.IntegerField(default=100)
    reply_limit = models.IntegerField(default=5)

    def filter_threads(self, filters=None):
        if filters:
            return self.threads.exclude(
                Q(expired=True) |
                Q(title__iregex=r'(' + '|'.join(filters) + ')')
            )
        return self.threads.exclude(expired=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.short_name)
        super(Board, self).save(*args, **kwargs)

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

    class Meta:
        # Order threads by bump count, using creation date as a tie breaker
        ordering = ('-bump_count', '-created_on')

    @cached_property
    def hit_reply_limit(self):
        # Returns True if Thread has passed it's reply limit
        replies = Reply.objects.filter(thread=self).count()
        if replies > self.board.reply_limit:
            return True
        return False

    @cached_property
    def get_absolute_url(self):
        return reverse(
            'boards:thread-detail', kwargs={
                'slug': self.board.slug,
                'pk': self.id
            }
        )

    def __str__(self):
        return self.title


class Reply(TimeStampedModel):
    replies = models.ManyToManyField("self", blank=True)
    thread = models.ForeignKey(Thread, related_name='replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    content = models.TextField(max_length=30000, blank=True, null=True)
    image = models.ImageField(
        upload_to='images/%Y/%m/%d',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('created_on',)

    def save(self, *args, **kwargs):
        self.thread.bump_count += 1
        self.thread.save(update_fields=['bump_count'])
        super(Reply, self).save(*args, **kwargs)

    def __str__(self):
        return self.content
