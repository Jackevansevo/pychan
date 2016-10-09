from boards.forms import ThreadCreateForm, ReplyForm
from boards.models import Board, Thread
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404


def index(request):
    return render(request, 'boards/index.html')


def board_detail(request, slug):
    board = get_object_or_404(Board, slug=slug)
    if request.method == 'POST':
        form = ThreadCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.board = board
            form.instance.image = form.cleaned_data['image']
            form.instance.save()
            return HttpResponseRedirect(board)
    else:
        form = ThreadCreateForm()
    filters = []
    if request.user.is_authenticated:
        filters = request.user.filters
    threads = board.filter_threads(filters)
    context = {'threads': threads, 'form': form}
    return render(request, 'boards/thread_list.html', context)


def thread_view(request, slug, pk):
    thread = get_object_or_404(Thread, pk=pk)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            form.instance.thread = thread
            form.instance.save()
            return HttpResponseRedirect(thread.get_absolute_url)
    else:
        form = ReplyForm()
    context = {'thread': thread, 'form': form}
    return render(request, 'boards/thread_detail.html', context)
