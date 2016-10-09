from django.template import Library

from boards.models import Board

register = Library()


@register.inclusion_tag('boards/board_list.html')
def show_boards():
    # Only need the slug and board name for the navbar links
    boards = Board.objects.all().values('slug', 'name')
    return {'boards': boards}
