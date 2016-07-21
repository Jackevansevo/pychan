from django.core.management.base import BaseCommand
from django.core.management import call_command
from autofixture import AutoFixture
from boards.models import Board, Thread, Reply

boards = {
    'g': 'Technology',
    'b': 'Random',
    'mu': 'Music',
    'v': 'Games',
    'fit': 'Fitness',
    'ck': 'Cooking'
}

# [TODO] Auto add random images, to Boards / Threads
# Emulate sample content of actual webpage


class Command(BaseCommand):
    """
    Populates the imageboard with fake test data
    """

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
        thread_fixture = AutoFixture(Thread)
        reply_fixture = AutoFixture(Reply)
        thread_fixture.create(10)
        reply_fixture.create(10)

        self.stdout.write(self.style.SUCCESS('Done'))
