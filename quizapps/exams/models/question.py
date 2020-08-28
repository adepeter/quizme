from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

limit_to = ~Q(questions__gte=10)

class Question(models.Model):
    story = models.ForeignKey(
        'exams.Story',
        verbose_name=_('story'),
        on_delete=models.CASCADE,
        related_name='questions',
        limit_choices_to=limit_to
    )
    question = models.TextField(_('question content'))

    def __str__(self):
        return self.question[:20]
