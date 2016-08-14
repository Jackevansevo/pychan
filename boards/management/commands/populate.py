from autofixture.generators import LoremWordGenerator, LoremSentenceGenerator
from autofixture import AutoFixture
from boards.models import Board, Thread, Reply
from django.core.files import File
from django.core.management import call_command
from django.core.management.base import BaseCommand

import os
import random

boards = {
    'b': 'Random',
    'ck': 'Cooking',
    'fit': 'Fitness',
    'g': 'Technology',
    'mu': 'Music',
    'v': 'Games',
}

# [TODO] Add random images Thread Replies
# Emulate sample content of actual webpage


class Command(BaseCommand):
    """
    Populates the imageboard with fake test data

    """
    def reaction_image(self):
        dir_path = "images/Reactions/"
        fp = dir_path + random.choice(os.listdir(os.path.abspath(dir_path)))
        return File(open(fp, 'rb'))

    help = 'Populates the database with mock data'

    def handle(self, *args, **options):
        self.stdout.write('Populating Database...')

        # Flush the Database of old data, suppress prompt
        call_command('flush', '--noinput')

        for key, val in boards.items():
            # Create a board
            board = Board.objects.create(name=val, short_name=key)
            board.save()

            # Load some random sample images
            dir_path = "images/" + str(board) + "/"
            images = os.listdir(os.path.abspath(dir_path))
            random.shuffle(images)

            titles = LoremWordGenerator(100)().split()
            contents = [LoremSentenceGenerator()() for i in range(100)]

            Thread.objects.bulk_create(
                Thread(
                    title=title,
                    content=content,
                    board=board,
                    image=File(open(dir_path + img, 'rb'))
                )
                for img, title, content in zip(images[:100], titles, contents)
            )

        reply_fixture = AutoFixture(
            Reply, field_values={'image': self.reaction_image})
        reply_fixture.create(1000)

        self.stdout.write(self.style.SUCCESS('Done'))
