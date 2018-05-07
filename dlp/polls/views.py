from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Poll, Choice
from .forms import ChoiceForm


MY_SCORE = 0


def pollview(request):
    latest_poll_list = Poll.objects.all()

    context = {
        'latest_poll_list': latest_poll_list,
    }
    return render(request, 'polls/pollview.html', context)


def pages(request, poll_id, page_idx):
    global MY_SCORE
    poll = get_object_or_404(Poll, pk=poll_id)
    all_pages = poll.page_set.all()
    page = all_pages.get(page_index=page_idx)

    random_questions = page.question_set.all().order_by('?')
    form = ChoiceForm(request.POST or None, questions=random_questions)

    if page == all_pages.last():
        if form.is_valid():
            for k in form.scores():
                MY_SCORE += int(k)

            return HttpResponseRedirect('/polls/result/poll/{}'.format(poll_id))

    else:
        next_page = all_pages.filter(page_index__gt=page.page_index).first().page_index

        if request.method == 'POST':
            if form.is_valid():
                for k in form.scores():
                    MY_SCORE += int(k)

                return HttpResponseRedirect('/polls/{}/page/{}'.format(poll_id, next_page))

    args = {'poll': poll, 'page': page, 'form': form, 'mp': ''}

    return render(request, 'polls/pages.html', args)


def result(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    global MY_SCORE
    temp_score = MY_SCORE
    MY_SCORE = 0
    admission_flag = False
    if temp_score >= poll.admission_score:
        admission_flag = True

    return render(request, 'polls/result.html', {'poll': poll, 'score': temp_score, 'admission_flag': admission_flag})
