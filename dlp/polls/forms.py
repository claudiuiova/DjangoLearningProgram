from django import forms


class ChoiceForm(forms.Form):

    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(ChoiceForm, self).__init__(*args, **kwargs)

        choices = []

        for q in questions:
            for choice in q.choice_set.all().order_by('?'):
                choices.append((choice.votes, choice.choice_text))

            self.fields[str(q.id)] = forms.ChoiceField(label=q.question_text, required=True,
                                                       choices=choices, widget=forms.RadioSelect())
            choices = []

    def scores(self):
        for q, a in self.cleaned_data.items():
            yield a
