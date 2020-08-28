from django import forms
from django.utils.translation import gettext_lazy as _


class AnswerForm(forms.Form):
    """Accepts story instance from view and make auto fields
    based on the questions.
    Reason for this is to be able to display all questions
    """
    def __init__(self, *args, **kwargs):
        story = kwargs.pop('story')
        super().__init__(*args, **kwargs)
        try:
            # return first 10 questions.
            # If generate field based on the available ones
            questions = story.questions.all()[10]
        except IndexError:
            questions = story.questions.all()
        for i, question in enumerate(questions):
            # make a  unique field with field name as question_QUESTIONID
            field = 'question_%s' % str(question.id)
            self.fields[field] = forms.ChoiceField(
                label=_(f'#{i+1} {question.question}'),
                choices=[(answer.id, answer.text) for answer in question.answers.all()],
                widget=forms.RadioSelect
            )