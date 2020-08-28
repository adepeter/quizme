from django.contrib import admin
from .models import Question, Answer, Story, Score


class AnswerStackedInline(admin.StackedInline):
    model = Answer
    extras = 5


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = [
        'headline',
        'content'
    ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'story',
        'question',
        'answer'
    ]
    inlines = [AnswerStackedInline]

    def answer(self, obj):
        answer = Answer.objects.get_answer_for_question(obj)
        return answer.text

    answer.short_description = 'Correct answer'


# @admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'text', 'is_answer']
    list_filter = ['question']


# @admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'value', 'story']