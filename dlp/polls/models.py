from django.db import models
from django.utils.translation import ugettext_lazy as _


class Poll(models.Model):
    poll_name = models.CharField(_("Poll Name"), max_length=200)
    pub_date = models.DateTimeField('date published')
    admission_score = models.IntegerField()
    attempts = models.IntegerField(default=0)
    passed_poll = models.IntegerField(default=0)

    class Meta:
        verbose_name = _("Poll")
        verbose_name_plural = _("Polls")

    def __str__(self):
        return self.poll_name

    def pass_rate(self):
        try:
            return "{}% pass rate".format(round(self.passed_poll / self.attempts * 100, 1))
        except ZeroDivisionError:
            return "no attempts on this poll"


class Page(models.Model):
    poll = models.ForeignKey(Poll, verbose_name=_("Poll"), on_delete=models.CASCADE)
    page_index = models.IntegerField(default=1)

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")
        ordering = ['page_index']


class Question(models.Model):
    page = models.ForeignKey(Page, verbose_name=_("Page"), on_delete=models.CASCADE)
    question_text = models.CharField(_("Question text"), max_length=200)

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, verbose_name=_("Question"),on_delete=models.CASCADE)
    choice_text = models.CharField(_("Choice text"), max_length=200)
    votes = models.IntegerField(_("Vote"), default=0)

    class Meta:
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")

    def __str__(self):
        return self.choice_text


class PollStats(models.Model):
    stats = models.CharField(_("Poll Stats"), max_length=200)

    def __str__(self):
        return self.stats
