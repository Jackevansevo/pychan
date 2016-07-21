from boards.forms import ThreadForm, ReplyForm
from boards.models import Board, Thread, Reply
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, CreateView


class BoardList(ListView):
    model = Board


class BoardDetail(DetailView):
    model = Board


class ThreadCreate(CreateView):
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


class ReplyCreate(CreateView):
    model = Reply
    form_class = ReplyForm
    template_name_suffix = "_create_form"

    def dispatch(self, request, *args, **kwargs):
        self.thread = Thread.objects.get(pk=self.kwargs['pk'])
        return super(ReplyCreate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.thread = self.thread
        return super(ReplyCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('boards:thread-detail', args=[self.thread.board.slug,
                                                     self.thread.pk])


class ThreadDetail(DetailView):
    model = Thread
