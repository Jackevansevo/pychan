from django.test import TestCase
from django.utils.html import escape
from django.core.urlresolvers import reverse
from boards.fixtures import (
    BoardFactory,
    ReplyFactory,
    ThreadFactory,
)

from boards.models import Thread
from boards.forms import ThreadCreateForm


class TestIndexView(TestCase):

    def setUp(self):
        self.url = reverse('boards:index')

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'boards/index.html')


class TestBoardDetail(TestCase):

    def setUp(self):
        self.board = BoardFactory(name='Technology')
        self.url = reverse('boards:board-detail', args=[self.board.slug])

    def test_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'boards/board_detail.html')

    def test_view_error_message_displayed_with_no_threads(self):
        response = self.client.get(self.url)
        expected_output = escape("No Threads Available")
        self.assertContains(response, expected_output)

    def test_view_queryset_with_with_no_threads(self):
        response = self.client.get(self.url)
        self.assertQuerysetEqual(response.context['threads'], [])

    def test_view_queryset_with_single_thread(self):
        ThreadFactory(board=self.board, title="test")
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            response.context['threads'],
            ['<Thread: test>']
        )

    def test_view_queryset_with_multiple_threads(self):
        ThreadFactory.create_batch(4, board=self.board)
        threads = Thread.objects.all()
        response = self.client.get(self.url)
        print(response.context)
        self.assertQuerysetEqual(
            response.context['threads'],
            ['<Thread: {}>'.format(t.title) for t in threads]
        )

    def test_form_appears_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], ThreadCreateForm)


class ThreadViewTests(TestCase):

    def setUp(self):
        self.thread = ThreadFactory()
        self.replies = ReplyFactory(thread=self.thread)
