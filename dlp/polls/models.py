from django.db import models
from django.utils import timezone
import datetime
from django.utils.translation import ugettext_lazy as _


class Poll(models.Model):
    poll_name = models.CharField(_("Poll Name"), max_length=200)
    pub_date = models.DateTimeField('date published')

    class Meta:
        verbose_name = _("Poll")
        verbose_name_plural = _("Polls")

    def __str__(self):
        return self.poll_name


class Page(models.Model):
    page = models.ForeignKey(Poll, verbose_name=_("Poll"), on_delete=models.CASCADE)
    page_index = models.CharField(_("Page index") ,max_length=200)

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = ("Pages")

class Question(models.Model):
    poll = models.ForeignKey(Page, verbose_name=_("Page"), on_delete=models.CASCADE)
    question_text = models.CharField(_("Question text") ,max_length=200)

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = ("Questions")

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, verbose_name=_("Question"),on_delete=models.CASCADE)
    choice_text = models.CharField(_("Choice text"), max_length=200)
    votes = models.IntegerField(_("Vote"), default=0)

    class Meta:
        verbose_name = ("Choice")
        verbose_name_plural = ("Choices")

    def __str__(self):
        return self.choice_text
