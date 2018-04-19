from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Poll, Choice, Question
from django.urls import reverse
from django.http import Http404

def index(request):
    latest_poll_list = Poll.objects.all()
    context = {
        'latest_poll_list': latest_poll_list,
    }
    return render(request, 'polls/index.html', context)

def detail(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'poll': poll})
