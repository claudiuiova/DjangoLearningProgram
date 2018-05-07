from django.contrib import admin
from .models import Question, Choice, Poll, Page
import nested_admin


class ChoiceInline(nested_admin.NestedStackedInline):
    model = Choice
    extra = 0


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 0
    inlines = [ChoiceInline]


class PageInline(nested_admin.NestedStackedInline):
    model = Page
    extra = 0
    inlines = [QuestionInline]


@admin.register(Poll)
class PollAdmin(nested_admin.NestedModelAdmin):
    fields = ["poll_name", "pub_date", "admission_score"]
    inlines = [PageInline]
