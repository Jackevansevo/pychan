from django.test import TestCase
from django.utils.html import escape
from django.core.urlresolvers import reverse
from boards.fixtures import (
    BoardFactory,
    ReplyFactory,
    ThreadFactory,
)

from boards.forms import ThreadCreateForm

from django.contrib.auth import get_user_model
User = get_user_model()


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
        threads = ThreadFactory.create_batch(4, board=self.board)
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            response.context['threads'],
            ['<Thread: {}>'.format(t.title) for t in threads],
            ordered=False
        )

    def test_form_appears_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], ThreadCreateForm)


class TestBoardFiltering(TestCase):
    def setUp(self):
        self.board = BoardFactory(name='Technology')
        self.url = reverse('boards:board-detail', args=[self.board.slug])
        self.user = User.objects.create_user('test', 'test@mail.com', 'secret')

    def test_thread_filtering_with_no_user_filters(self):
        threads = ThreadFactory.create_batch(4, board=self.board)
        self.client.login(username='test', password='secret')
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            response.context['threads'],
            ['<Thread: {}>'.format(t.title) for t in threads],
            ordered=False
        )

    def test_thread_filtering_with_single_filter(self):
        ThreadFactory.create_batch(4, board=self.board, title="meme")
        shown = ThreadFactory.create_batch(4, board=self.board)

        self.user.filters = ['meme']
        self.user.save(update_fields=['filters'])
        self.client.login(username='test', password='secret')

        response = self.client.get(self.url)

        self.assertQuerysetEqual(
            response.context['threads'],
            ['<Thread: {}>'.format(t.title) for t in shown],
            ordered=False
        )

    def test_thread_filtering_with_multiple_filters(self):
        ThreadFactory(board=self.board, title="meme")
        ThreadFactory(board=self.board, title="test")
        shown = ThreadFactory.create_batch(4, board=self.board, title="shown")

        self.user.filters = ['meme', 'test']
        self.user.save(update_fields=['filters'])
        self.client.login(username='test', password='secret')

        response = self.client.get(self.url)

        self.assertQuerysetEqual(
            response.context['threads'],
            ['<Thread: {}>'.format(t.title) for t in shown],
            ordered=False
        )


class ThreadViewTests(TestCase):

    def setUp(self):
        self.thread = ThreadFactory()
        self.replies = ReplyFactory(thread=self.thread)
