from django.db import models


class AnswerManager(models.Manager):
    def get_answer_for_question(self, question, is_answer=True):
        return self.get(question=question, is_answer=is_answer)
