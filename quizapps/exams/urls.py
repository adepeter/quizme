from django.urls import path

from . import views

urlpatterns = [
    path('', views.StoryListView.as_view(), name='story_list'),
    path('<int:story_id>/', views.ExamView.as_view(), name='list_questions'),
    path('<int:story_id>/instructions/', views.read_instruction, name='instruction'),
    path('success/', views.SuccessView.as_view(), name='exam_completed'),
]
