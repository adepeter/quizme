from django.db import models
from django.utils.translation import gettext_lazy as _

class Question(models.Model):
    story = models.ForeignKey(
        'exams.Story',
        verbose_name=_('story'),
        on_delete=models.CASCADE,
        related_name='questions',
    )
    question = models.TextField(_('question content'))

    def __str__(self):
        return self.question[:20]
