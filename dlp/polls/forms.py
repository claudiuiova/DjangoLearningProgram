from django import forms
from polls.models import Poll, Page, Question, Choice

# CHOICES = []

# def get_choices(id):
#     CHOICES = []
#     poll = Poll.objects.get(pk = id)
#     for


class QuestionForm(forms.ModelForm):

    class Meta:
        model = Choice
        fields = ('choice_text', )
