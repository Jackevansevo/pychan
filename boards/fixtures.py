from faker import Factory as FakerFactory

from boards.models import Board, Reply, Thread
from boards.providers import ImageProvider

import factory
import os


faker = FakerFactory.create('en_GB')

faker.add_provider(ImageProvider)


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board
    name = factory.LazyAttribute(lambda x: faker.word())
    short_name = factory.LazyAttribute(lambda x: x.name[:1].strip())


class ThreadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Thread

    title = factory.LazyAttribute(lambda x: faker.sentence())
    content = factory.LazyAttribute(lambda x: "".join(faker.sentences()))
    image = factory.LazyAttribute(
        lambda x: faker.image(os.path.join("images", x.board.name))
    )
    board = factory.Iterator(Board.objects.all())


class ReplyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reply

    thread = factory.Iterator(Thread.objects.all())
    content = factory.LazyAttribute(lambda x: faker.sentence())
    image = factory.LazyAttribute(
        lambda x: faker.image(os.path.join("images", "Reactions"))
    )
