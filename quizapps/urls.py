from django.contrib.auth.views import LoginView
from django.urls import include, path

urlpatterns = [
    path('', include('quizapps.exams.urls')),
    path('login/', LoginView.as_view(), name='login'),
]