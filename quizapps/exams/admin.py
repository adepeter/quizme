import markdown
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Question, Answer, Story, Score


class AnswerStackedInline(admin.StackedInline):
    model = Answer
    extras = 5

class QuestionStackedInline(admin.StackedInline):
    model = Question
    extras = 10


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = [
        'headline',
    ]
    readonly_fields = ['passage']
    inlines = [QuestionStackedInline]

    def passage(self, obj):
        return mark_safe(markdown.markdown(obj.content))
    passage.short_description = 'Passage preview'


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