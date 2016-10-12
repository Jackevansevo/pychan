from django.test import TestCase
from django.core.urlresolvers import reverse
from boards.fixtures import (
    BoardFactory,
    ReplyFactory,
    ThreadFactory,
)


class BoardDetailTests(TestCase):

    def setUp(self):
        self.board = BoardFactory()
        self.url = reverse('boards:board-detail', args=[self.board.slug])
        pass

    def test_view_uses_correct_template(self):
        pass

    def test_view_with_with_no_threads(self):
        pass

    def test_view_with_single_thread(self):
        pass

    def test_view_with_multiple_threads(self):
        pass

    def test_form_appears_in_context(self):
        pass

    def test_view_filters_for_user(self):
        pass


class ThreadViewTests(TestCase):

    def setUp(self):
        self.thread = ThreadFactory()
        self.replies = ReplyFactory(thread=self.thread)
