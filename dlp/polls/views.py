from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Poll, Choice, Question, Page
from .forms import ChoiceForm, QuestionForm

def pollview(request):
    latest_poll_list = Poll.objects.all()
    context = {
        'latest_poll_list': latest_poll_list,
    }
    return render(request, 'polls/pollview.html', context)

def pages(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/pages.html', {'poll': poll})

def questions(request, page_id):
    page = get_object_or_404(Page, pk=page_id)
    return render(request, 'polls/pageview.html', {'page': page})

