from django.db import models
from django.utils.translation import gettext_lazy as _

from ..managers.answer import AnswerManager


class Answer(models.Model):
    question = models.ForeignKey(
        'exams.Question',
        verbose_name=_('question'),
        on_delete=models.CASCADE,
        related_name='answers'
    )
    text = models.TextField(verbose_name=_('answer text'))
    is_answer = models.BooleanField(default=False)

    objects = AnswerManager()

    def __str__(self):
        return f'{self.text} - {self.is_answer}'