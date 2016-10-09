from django.core.files import File
from django.core.management import call_command
from django.core.management.base import BaseCommand

from boards.fixtures import ThreadFactory, ReplyFactory
from boards.models import Board

import os
import random

boards = {
    'b': 'Random',
    'g': 'Technology',
}


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

            # Create some threads
            ThreadFactory.create_batch(100, board=board)

        ReplyFactory.create_batch(1000)

        self.stdout.write(self.style.SUCCESS('Done'))
