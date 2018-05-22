from django import forms
from django.shortcuts import get_object_or_404
from .models import Question


class ChoiceForm(forms.Form):

    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(ChoiceForm, self).__init__(*args, **kwargs)

        choices = []

        for q in questions:
            for choice in q.choice_set.all().order_by('?'):
                choices.append((choice.id, choice.choice_text))

            self.fields[str(q.id)] = forms.ChoiceField(label=q.question_text,
                                                       choices=choices, widget=forms.RadioSelect())
            choices = []

    def selected_answers(self):
        for q_id, c_id in self.cleaned_data.items():
            yield (q_id, c_id)


class ResultForm(forms.Form):
    def __init__(self, *args, **kwargs):
        poll = kwargs.pop('poll')
        post_data = kwargs.pop('post_data')
        super(ResultForm, self).__init__(*args, **kwargs)

        self.choices = []
        self.correct_answers_list = []

        for pg in poll.page_set.all():
            for q in pg.question_set.all():
                q.question_attempts += 1
                q.save()
                for c in q.choice_set.all():
                    if c.votes == 1:
                        self.correct_answers_list.append(str(c.id))
                    self.choices.append((str(c.id), c.choice_text))

                self.fields[q.id] = forms.ChoiceField(label=q.question_text, choices=self.choices,
                                                      initial=post_data[str(q.id)],
                                                      widget=forms.RadioSelect())
                self.fields[q.id].widget.attrs['disabled'] = 'disabled'

                self.choices = []

        for q_id, c_id in post_data.items():
            if str(c_id) in self.correct_answers_list:
                question = get_object_or_404(Question, pk=int(q_id))
                question.correct_answers += 1
                question.save()
