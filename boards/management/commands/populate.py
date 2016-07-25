from autofixture import AutoFixture
from boards.models import Board, Thread, Reply
from django.core.files import File
from django.core.management import call_command
from django.core.management.base import BaseCommand

import os
import random

boards = {
    'g': 'Technology',
    'b': 'Random',
    'mu': 'Music',
    'v': 'Games',
    'fit': 'Fitness',
    'ck': 'Cooking'
}

# [TODO] Add random images Thread Replies
# Emulate sample content of actual webpage


class Command(BaseCommand):
    """
    Populates the imageboard with fake test data

    """
    def random_image(self):
        fp = "images/" + random.choice(os.listdir(os.path.abspath("images")))
        return File(open(fp, 'rb'))

    help = 'Populates the database with mock data'

    def handle(self, *args, **options):
        self.stdout.write('Populating Database...')

        # Flush the Database of old data, suppress prompt
        call_command('flush', '--noinput')

        # Create a Board instance each item in the boards dictionary
        Board.objects.bulk_create(
            Board(name=val, short_name=key) for key, val in boards.items()
        )

        # Randomly generate threads and replies for existing boards
        thread_fixture = AutoFixture(
            Thread, field_values={'image': self.random_image})
        reply_fixture = AutoFixture(
            Reply, field_values={'image': self.random_image})
        thread_fixture.create(100)
        reply_fixture.create(500)

        self.stdout.write(self.style.SUCCESS('Done'))
