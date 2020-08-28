from django.db import models


class Story(models.Model):
    headline = models.CharField(max_length=20)
    instruction = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name_plural = 'Stories'

    def __str__(self):
        return self.headline
