from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.sessions.models import Session
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .models import Poll, Choice, PollStats
from .forms import ChoiceForm, ResultForm
from datetime import datetime, timezone


def home(request):
    return render(request, 'polls/home.html', {})


def statistics(request):
    if request.user.is_authenticated:
        return render(request, 'polls/statistics.html', {})
    else:
        return HttpResponseRedirect('login')


def login_as_admin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            this_user = form.get_user()
            login(request, this_user)
            return HttpResponseRedirect('statistics')
    else:
        form = AuthenticationForm()

    return render(request, 'polls/admin_login.html', {'form': form})


def poll_attempts(request):
    latest_poll_list = Poll.objects.all()
    return render(request, 'polls/poll_attempts.html', {'polls': latest_poll_list})


def pollview_stats(request):
    latest_poll_list = Poll.objects.all()
    return render(request, 'polls/pollview_stats.html', {'latest_poll_list': latest_poll_list})


def statistics_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    poll_stats = PollStats.objects.all()
    users = []

    for obj in poll_stats:
        for user, res in eval(obj.stats).items():
            if res['poll_id'] == poll.id:
                users.append(user)
    if len(users) == 0:
        return HttpResponse("not attempts on this poll")
    return render(request, 'polls/polls_users.html', {'stats': users, 'poll': poll})


def most_wrong_questions_polls(request):
    latest_poll_list = Poll.objects.all()
    return render(request, 'polls/mostwrongquestions_polls.html', {'latest_poll_list': latest_poll_list})


def most_wrong_questions_results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/mwq_results.html', {'poll': poll})


def user_result(request, poll_id, user):
    poll_stats = PollStats.objects.all()
    poll = get_object_or_404(Poll, pk=poll_id)

    for obj in poll_stats:
        for usr, res in eval(obj.stats).items():
            if usr == user:
                poll_stats = {user: res}
                break

    form = ResultForm(poll=poll, post_data=poll_stats[user]['pdata'])

    args = {'poll': poll, 'score': poll_stats[user]['score'], 'admission_flag': poll_stats[user]['admission_flag'],
            'post_data': poll_stats[user]['pdata'], 'form': form, 'correct_answers': form.correct_answers_list}

    return render(request, 'polls/result.html', args)


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

    my_data = PollStats(stats={
                                request.session.session_key: {
                                    'poll_id': poll_id,
                                    'admission_score': poll.admission_score,
                                    'admission_flag': admission_flag,
                                    'pdata': request.session['pdata'],
                                    'score': request.session['score']
                                }
                            })
    my_data.save()
    request.session.set_expiry(7200)
    return render(request, 'polls/result.html', args)
