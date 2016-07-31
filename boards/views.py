from boards.forms import ThreadForm, ReplyForm
from boards.models import Board, Thread, Reply, Filter
from django.core.urlresolvers import reverse
from django.http import HttpResponseNotFound
from django.views.generic import ListView, DetailView, CreateView, View

# [TODO] Be consistent with kwargs and args in get_absolute_url()
# [TODO] Save colour scheme in session cookie, then load in base.html


class ShowBoardsMixin(View):
    def get_boards(self):
        # To display a list of boards at the top of each view
        return Board.objects.all()


class BoardList(ShowBoardsMixin, ListView):
    model = Board


class BoardDetail(ShowBoardsMixin, DetailView):
    model = Board

    def get_threads(self):
        threads = Thread.active_threads.filter(board=self.object)
        if self.request.user.is_authenticated():
            # Get a list of user defined text filters
            filter_list = Filter.objects.filter(
                user=self.request.user).values_list('text', flat=True)
            # Loop through user filters and exclude matching threads
            for filter_text in filter_list:
                threads = threads.exclude(title__icontains=filter_text)
        return threads


class ThreadCreate(ShowBoardsMixin, CreateView):
    model = Thread
    form_class = ThreadForm
    template_name_suffix = "_create_form"

    def dispatch(self, request, *args, **kwargs):
        self.board = Board.objects.get(slug=self.kwargs['slug'])
        return super(ThreadCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.board = self.board
        return super(ThreadCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('boards:board-detail', args=[self.board.slug])


class ReplyCreate(ShowBoardsMixin, CreateView):
    model = Reply
    form_class = ReplyForm
    template_name_suffix = "_create_form"

    def dispatch(self, request, *args, **kwargs):
        self.thread = Thread.objects.get(pk=self.kwargs['pk'])
        if self.thread.has_404d:
            return HttpResponseNotFound('<h1>Thread has 404d</h1>')
        return super(ReplyCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.thread = self.thread
        return super(ReplyCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('boards:thread-detail', args=[self.thread.board.slug,
                                                     self.thread.pk])


class ThreadDetail(ShowBoardsMixin, DetailView):
    model = Thread

    def get_object(self):
        # Cache the object in order to check it at dispatch
        if not hasattr(self, '_object'):
            self._object = super(ThreadDetail, self).get_object()
        return self._object

    def dispatch(self, request, *args, **kwargs):
        # Check if the thread has 404'd or not
        if self.get_object().has_404d:
            return HttpResponseNotFound('<h1>Thread has 404d</h1>')
        return super(ThreadDetail, self).dispatch(request, *args, **kwargs)
