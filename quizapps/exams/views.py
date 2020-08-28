from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, FormView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.utils import timezone

from .forms import AnswerForm
from .models import Answer, Score, Story

TEST_TIMEOUT = settings.TEST_TIMEOUT


class StoryListView(ListView):
    model = Story
    context_object_name = 'stories'
    template_name = 'exams/stories.html'


class ExamView(LoginRequiredMixin, SingleObjectMixin, FormView):
    model = Story
    form_class = AnswerForm
    template_name = 'exams/questions.html'
    context_object_name = 'story'
    pk_url_kwarg = 'story_id'
    success_url = reverse_lazy('exam_completed')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        cache.set('time_start', timezone.now(), TEST_TIMEOUT)
        return super().get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'story': self.get_object()})
        return kwargs

    def post(self, request, *args, **kwargs):
        if cache.get('time_start') is None:
            return HttpResponse('<b>Time for test exceeded</b>')
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        story = self.get_object()
        questions = story.questions.all()
        answers = Answer.objects.filter(question__in=questions, is_answer=True)
        serialize_answers = {f'question_{answer.question.id}': str(answer.id) \
                             for answer in answers}
        serialize_questions = [f'question_{question.id}' for question in questions]
        scores = 0
        for field in serialize_questions:
            if form.cleaned_data[field] == serialize_answers[field]:
                scores += 5
        Score.objects.create(user=self.request.user, story=story, value=scores)
        self.request.session[self.request.user.username] = scores
        return super().form_valid(form)


class SuccessView(TemplateView):
    template_name = 'exams/success_exam.html'

    def get(self, request, *args, **kwargs):
        try:
            self.get_score = request.session.pop(request.user.username)
        except KeyError:
            raise Http404('You got here by mistake. \
            You probably might have taken the test')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['score'] = self.get_score
        return context


def read_instruction(request, story_id):
    story = get_object_or_404(Story, pk=story_id)
    if request.method == 'POST':
        kwargs = {
            'story_id': story.id
        }
        return HttpResponseRedirect(reverse('list_questions', kwargs=kwargs))
    return render(request, 'exams/instruction.html', {'story': story})
