from django.urls import path

from aonebrains_quiz.views import QuizCreateUpdateView, MCQCreateUpdateView, QuizListView, MCQListView, QuizDetailView, \
    MCQDetailView

app_name = "aonebrains_quiz"

urlpatterns = [

    path('<slug:slug>/quiz/detail/', QuizDetailView.as_view(), name='quiz_detail'),
    path('<int:pk>/Question/detail/', MCQDetailView.as_view(), name='mcq_detail'),
    path('<slug:course_slug>/quiz/create/', QuizCreateUpdateView.as_view(), name='quiz_create'),
    path('<slug:course_slug>/quiz/<slug:quiz_slug>/edit/', QuizCreateUpdateView.as_view(), name='quiz_edit'),
    path('<slug:course_slug>/quiz/<slug:quiz_slug>/mcq/create/', MCQCreateUpdateView.as_view(), name='mcq_create'),
    path('<slug:course_slug>/quiz/<slug:quiz_slug>/mcq/<int:mcq_id>/edit/', MCQCreateUpdateView.as_view(),
         name='mcq_edit'),
    path('<slug:course_slug>/quizzes/', QuizListView.as_view(), name='quiz_list'),
    path('<slug:course_slug>/quiz/<slug:quiz_slug>/mcqs/', MCQListView.as_view(), name='mcq_list')

]
