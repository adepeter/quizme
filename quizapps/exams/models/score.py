from django.db import models
from django.contrib.auth.models import User


class Score(models.Model):
    value = models.PositiveSmallIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scores')
    story = models.ForeignKey('exams.Story', on_delete=models.CASCADE, related_name='scores')

    def __str__(self):
        return f'{self.value} - {self.user}'
