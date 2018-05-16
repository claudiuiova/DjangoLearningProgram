from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Poll, Choice
from .forms import ChoiceForm, ResultForm
from datetime import datetime, timezone
from django.contrib.sessions.models import Session


def home(request):
    return render(request, 'polls/home.html', {})


def statistics(request):
    return render(request, 'polls/statistics.html', {})


def poll_attempts(request):
    latest_poll_list = Poll.objects.all()
    return render(request, 'polls/poll_attempts.html', {'polls': latest_poll_list})


def pollview(request):
    latest_poll_list = Poll.objects.all()

    for _session in Session.objects.all():
        if datetime.now(timezone.utc) > _session.expire_date:
            _session.delete()
    request.session.create()

    context = {
        'latest_poll_list': latest_poll_list,
    }
    return render(request, 'polls/pollview.html', context)


def pages(request, poll_id, page_idx):

    if not request.session.get('score'):
        request.session['score'] = 0

    if not request.session.get('pdata'):
        request.session['pdata'] = {}

    if not request.session.get('correct_answers'):
        request.session['correct_answers'] = []

    poll = get_object_or_404(Poll, pk=poll_id)
    all_pages = poll.page_set.all()
    page = all_pages.get(page_index=page_idx)

    random_questions = page.question_set.all().order_by('?')
    form = ChoiceForm(request.POST or None, questions=random_questions)
    button_text = 'Next'

    if page == all_pages.last():
        button_text = 'Submit'

        if form.is_valid():
            for q_id, c_id in form.selected_answers():
                request.session['pdata'].update({q_id: c_id})
                request.session['score'] += get_object_or_404(Choice, pk=c_id).votes

            return HttpResponseRedirect('/polls/poll{}/results'.format(poll_id))

    else:
        next_page = all_pages.filter(page_index__gt=page.page_index).first().page_index

        if request.method == 'POST':
            if form.is_valid():
                for q_id, c_id in form.selected_answers():
                    request.session['pdata'].update({q_id: c_id})
                    request.session['score'] += get_object_or_404(Choice, pk=c_id).votes

                return HttpResponseRedirect('/polls/{}/page/{}'.format(poll_id, next_page))

    args = {'poll': poll, 'page': page, 'form': form, 'mp': '', 'btn': button_text}
    return render(request, 'polls/pages.html', args)


def result(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    poll.attempts += 1

    admission_flag = False
    if request.session['score'] >= poll.admission_score:
        poll.passed_poll += 1
        admission_flag = True

    poll.save()
    form = ResultForm(poll=poll, post_data=request.session['pdata'])

    args = {'poll': poll, 'score': request.session['score'], 'admission_flag': admission_flag,
            'post_data': request.session['pdata'], 'form': form, 'correct_answers': form.correct_answers_list}

    request.session.set_expiry(7200)
    return render(request, 'polls/result.html', args)
