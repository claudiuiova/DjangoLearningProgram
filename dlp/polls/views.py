from django.shortcuts import render, get_object_or_404
from .models import Poll


def pollview(request):
    latest_poll_list = Poll.objects.all()
    
    context = {
        'latest_poll_list': latest_poll_list,
    }
    return render(request, 'polls/pollview.html', context)


def pages(request, poll_id, page_index):
    poll = get_object_or_404(Poll, pk=poll_id)
    all_pages = poll.page_set.all()
    page = all_pages.get(page_index=page_index)

    next_page = page_index + 1
    args = {'poll': poll, 'page': page, 'next_page': next_page}

    return render(request, 'polls/pages.html', args)


def result(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/result.html', {'poll': poll})
