from django.urls import path

from aonebrains_main.views import Home, AllCoursesListView, CourseDetailView, \
    StudentCourseDetailView, StudentCourseListView, SchoolCoursesListView, SchoolCourseDetailView, \
    SchoolStudentCourseDetailView, SchoolStudentCourseListView, ProfileView
from aonebrains_quiz.views import QuizTake, QuizStudentProgressView
from school_quiz import views as school_quiz_view

app_name = "aonebrains_main"

urlpatterns = [
    path('', Home.as_view(), name="Home"),
    path('profile/', ProfileView.as_view(), name='profile'),
    path("courses/", AllCoursesListView.as_view(), name="course_list"),
    path("course/<slug:course_slug>/", CourseDetailView.as_view(), name="course_detail"),
    path('student/course/<slug:course_slug>/', StudentCourseDetailView.as_view(),
         name='student_course_detail'),
    path("quiz/<slug:quiz_slug>", QuizTake.as_view(), name='quiz_question'),
    path("quiz/progress/", QuizStudentProgressView.as_view(), name='quiz_progress'),
    path('student/courses/', StudentCourseListView.as_view(),
         name='student_course_list'),

    # School
    path('school/courses/', SchoolCoursesListView.as_view(), name="school_course_list"),
    path("school/course/<slug:course_slug>/", SchoolCourseDetailView.as_view(), name="school_course_detail"),
    path('school/student/course/<slug:course_slug>/', SchoolStudentCourseDetailView.as_view(),
         name='school_student_course_detail'),
    path('school/student/courses/', SchoolStudentCourseListView.as_view(),
         name='school_student_course_list'),
    path("school/quiz/<slug:quiz_slug>", school_quiz_view.QuizTake.as_view(), name='school_quiz_question'),
    path("school/quiz/progress/", school_quiz_view.QuizStudentProgressView.as_view(), name='school_quiz_progress'),

]
