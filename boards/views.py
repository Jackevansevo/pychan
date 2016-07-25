from boards.forms import ThreadForm, ReplyForm
from boards.models import Board, Thread, Reply, Filter
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, View


class ShowBoardsMixin(View):
    def get_boards(self):
        # To display a list of boards at the top of each view
        return Board.objects.all()


class BoardList(ShowBoardsMixin, ListView):
    model = Board


class BoardDetail(ShowBoardsMixin, DetailView):
    model = Board

    def get_threads(self):
        threads = Thread.objects.filter(board=self.object)
        if self.request.user.is_authenticated():
            # Get a list of user defined text filters
            filter_list = Filter.objects.filter(
                user=self.request.user).values_list('text', flat=True)
            # Loop through the filters and filter down the thread queryset
            for filter_text in filter_list:
                threads = threads.filter(~Q(title__icontains=filter_text))
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
