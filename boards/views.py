from boards.forms import ThreadCreateForm, ReplyForm
from boards.models import Board, Thread
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView, View, FormView
from django.views.generic.detail import SingleObjectMixin

# [TODO] Be consistent with kwargs and args in get_absolute_url()
# [TODO] Save colour scheme in session cookie, then load in base.html


class ShowBoardsMixin(View):
    def get_boards(self):
        # To display a list of boards at the top of each view
        return Board.objects.all()


class BoardList(ShowBoardsMixin, ListView):
    model = Board


class BoardDisplay(ShowBoardsMixin, DetailView):
    model = Board

    def get_context_data(self, **kwargs):
        context = super(BoardDisplay, self).get_context_data(**kwargs)
        context['form'] = ThreadCreateForm()
        user_filters = None
        if self.request.user.is_authenticated():
            user_filters = self.request.user.filters
        context['threads'] = self.object.get_threads(filters=user_filters)
        return context


class ThreadCreate(SingleObjectMixin, FormView):
    template_name = 'boards/board_detail.html'
    form_class = ThreadCreateForm
    model = Board

    # [TODO] Stick this in a super class, from which both Thread views inherit
    def get_context_data(self, **kwargs):
        context = super(ThreadCreate, self).get_context_data(**kwargs)
        user_filters = None
        if self.request.user.is_authenticated():
            user_filters = self.request.user.filters
        context['threads'] = self.object.get_threads(filters=user_filters)
        return context

    def post(self, request, *args, **kwargs):
        self.object = Board.objects.get(slug=self.kwargs['slug'])
        return super(ThreadCreate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.board = self.object
        obj.save()
        return super(ThreadCreate, self).form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url


class BoardDetail(View):

    def get(self, request, *args, **kwargs):
        view = BoardDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ThreadCreate.as_view()
        return view(request, *args, **kwargs)


class ThreadDisplay(ShowBoardsMixin, DetailView):
    model = Thread

    def get_context_data(self, **kwargs):
        context = super(ThreadDisplay, self).get_context_data(**kwargs)
        context['form'] = ReplyForm()
        return context


class ReplyToThread(SingleObjectMixin, FormView):
    template_name = 'boards/thread_detail.html'
    form_class = ReplyForm
    model = Thread

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(ReplyToThread, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.thread = self.object
        reply.save()
        return super(ReplyToThread, self).form_valid(form)

    def get_success_url(self):
        return reverse('boards:thread-detail', args=[self.object.board.slug,
                                                     self.object.pk])


class ThreadDetail(View):

    def get(self, request, *args, **kwargs):
        view = ThreadDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ReplyToThread.as_view()
        return view(request, *args, **kwargs)
