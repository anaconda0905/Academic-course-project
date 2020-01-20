from django.urls import path, include

#
from school_courses.views import CourseListView, CourseDetailView, CourseCreateView, ManageCourseListView, \
    CourseUpdateView, \
    ModuleCreateUpdateView, ContentCreateUpdateView, ContentDeleteView, ModuleListView, ContentOrderView, \
    ModuleOrderView, CourseDeleteView, ModuleContentListView
from school_quiz.views import QuizListView, MCQListView, MCQCreateUpdateView, QuizCreateUpdateView
from .views import SchoolSignUpView, ProfileView, StudentListView, StudentDetailView, \
    TeacherListView, TeacherDetailView, StudentEnrollCourseView, StudentCourseListView, \
    StudentCourseDetailView, SchoolListView, SchoolDetailView, SchoolDashboard, TeacherDashboard, \
    RegisterMultipleStudentsParseExcel

# noinspection PyUnresolvedReferences
urlpatterns = [
    path('school/', include(([
                                 path('dashboard/', SchoolDashboard.as_view(), name='dashboard'),
                                 path('list/', SchoolListView.as_view(), name='schools_list'),
                                 path('<str:slug>/detail/', SchoolDetailView.as_view(), name='school_detail'),
                                 path('sign_up/', SchoolSignUpView.as_view(), name='signup'),
                                 path('profile/', ProfileView.as_view(), name='profile'),
                                 path('<slug:school_slug>/students/list/', StudentListView.as_view(),
                                      name='school_student_list'),
                                 path('<slug:school_slug>/teachers/list/', TeacherListView.as_view(),
                                      name='school_teacher_list'),
                                 path('courses/', include(([
                                                               path('list/', CourseListView.as_view(),
                                                                    name='course_list'),
                                                               path('subject/<slug:subject>/', CourseListView.as_view(),
                                                                    name='course_list_subject'),
                                                               # path('<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
                                                               path('module/<int:course_id>/', ModuleListView.as_view(),
                                                                    name='module_list'),
                                                               path('<pk>/delete/', CourseDeleteView.as_view(),
                                                                    name='course_delete'),
                                                               path('module/<int:module_id>/content/list',
                                                                    ModuleContentListView.as_view(),
                                                                    name='module_content_list'),
                                                           ], 'courses'), namespace='courses')),

                                 path('student/', include(([
                                                               # path('sign_up/', StudentSignUpView.as_view(), name='signup'),
                                                               path('bulk/register/',
                                                                    RegisterMultipleStudentsParseExcel.as_view(),
                                                                    name='student_bulk_register'),
                                                               path('list/', StudentListView.as_view(), name='list'),
                                                               path('detail/<int:pk>/', StudentDetailView.as_view(),
                                                                    name="detail"),
                                                               path('profile/', ProfileView.as_view(), name='profile'),
                                                               path('enroll-course/', StudentEnrollCourseView.as_view(),
                                                                    name='student_enroll_course'),
                                                               path('courses/', StudentCourseListView.as_view(),
                                                                    name='student_course_list'),
                                                               path('course/<pk>/', StudentCourseDetailView.as_view(),
                                                                    name='student_course_detail'),
                                                               path('course/<pk>/<module_id>/',
                                                                    StudentCourseDetailView.as_view(),
                                                                    name='student_course_detail_module'),
                                                           ], 'students'), namespace='students')),

                                 path('teacher/', include(([
                                                               path('dashboard/', TeacherDashboard.as_view(),
                                                                    name='dashboard'),
                                                               path('list/', TeacherListView.as_view(), name='list'),
                                                               path('detail/<int:pk>/', TeacherDetailView.as_view(),
                                                                    name='detail'),
                                                               path('profile/', ProfileView.as_view(), name='profile'),
                                                               path('courses/', include(([
                                                                                             path('mine/',
                                                                                                  ManageCourseListView.as_view(),
                                                                                                  name='manage_course_list'),
                                                                                             path('create/',
                                                                                                  CourseCreateView.as_view(),
                                                                                                  name='course_create'),
                                                                                             path('<pk>/edit/',
                                                                                                  CourseUpdateView.as_view(),
                                                                                                  name='course_edit'),
                                                                                             path('<pk>/delete/',
                                                                                                  CourseDeleteView.as_view(),
                                                                                                  name='course_delete'),
                                                                                             path(
                                                                                                 '<int:course_id>/module/create/',
                                                                                                 ModuleCreateUpdateView.as_view(),
                                                                                                 name='course_module_create'),
                                                                                             path(
                                                                                                 '<int:course_id>/module/<int:module_id>/',
                                                                                                 ModuleCreateUpdateView.as_view(),
                                                                                                 name='course_module_update'),
                                                                                             path(
                                                                                                 'module/<int:module_id>/content/<model_name>/create/',
                                                                                                 ContentCreateUpdateView.as_view(),
                                                                                                 name='module_content_create'),
                                                                                             path(
                                                                                                 'module/<int:module_id>/content/<model_name>/<int:id>/',
                                                                                                 ContentCreateUpdateView.as_view(),
                                                                                                 name='module_content_update'),
                                                                                             path(
                                                                                                 'content/<int:id>/delete/',
                                                                                                 ContentDeleteView.as_view(),
                                                                                                 name='module_content_delete'),
                                                                                             path(
                                                                                                 'module/<int:course_id>/',
                                                                                                 ModuleListView.as_view(),
                                                                                                 name='module_list'),
                                                                                             path(
                                                                                                 'module/<int:module_id>/content/list',
                                                                                                 ModuleContentListView.as_view(),
                                                                                                 name='module_content_list'),
                                                                                             path('module/order/',
                                                                                                  ModuleOrderView.as_view(),
                                                                                                  name='module_order'),
                                                                                             path('content/order/',
                                                                                                  ContentOrderView.as_view(),
                                                                                                  name='content_order'),
                                                                                             path(
                                                                                                 'subject/<slug:subject>/',
                                                                                                 CourseListView.as_view(),
                                                                                                 name='course_list_subject'),
                                                                                             path('<slug:slug>/',
                                                                                                  CourseDetailView.as_view(),
                                                                                                  name='course_detail'),
                                                                                             path(
                                                                                                 '<int:course_id>/quiz/create/',
                                                                                                 QuizCreateUpdateView.as_view(),
                                                                                                 name='quiz_create'),
                                                                                             path(
                                                                                                 '<int:course_id>/quiz/<int:quiz_id>/edit/',
                                                                                                 QuizCreateUpdateView.as_view(),
                                                                                                 name='quiz_edit'),
                                                                                             path(
                                                                                                 '<int:course_id>/quiz/<int:quiz_id>/mcq/create/',
                                                                                                 MCQCreateUpdateView.as_view(),
                                                                                                 name='mcq_create'),
                                                                                             path(
                                                                                                 '<int:course_id>/quiz/<int:quiz_id>/mcq/<int:mcq_id>/edit/',
                                                                                                 MCQCreateUpdateView.as_view(),
                                                                                                 name='mcq_edit'),
                                                                                             path(
                                                                                                 '<int:course_id>/quizzes/',
                                                                                                 QuizListView.as_view(),
                                                                                                 name='quiz_list'),
                                                                                             path(
                                                                                                 '<int:course_id>/quiz/<int:quiz_id>/mcqs/',
                                                                                                 MCQListView.as_view(),
                                                                                                 name='mcq_list')
                                                                                         ], 'courses'),
                                                                   namespace='courses')),

                                                               path('student/', include(([
                                                                                             path('list/',
                                                                                                  StudentListView.as_view(),
                                                                                                  name='list'),
                                                                                             # path('add/', TeacherStudentAddView.as_view(), name='add'),
                                                                                             path('detail/<int:pk>/',
                                                                                                  StudentDetailView.as_view(),
                                                                                                  name="detail"),
                                                                                         ], 'students'),
                                                                   namespace='students')),
                                                           ], 'teachers'), namespace='teachers')), ], 'schools'))),
]

#
# app_name = "schools"
#
# # noinspection PyUnresolvedReferences
# urlpatterns = [
#     path("sign-up/", SchoolSignUpView.as_view(), name="school_sign_up"),
#     path("list/", StudentListView.as_view(), name="schools_list"),
#     path("dashboard/", SchoolDashboard.as_view(), name="school_dashboard"),
#     path("<slug:slug>/", SchoolDetailView.as_view(), name="school_detail"),
#         path('courses/', include(([
#             path('list/', CourseListView.as_view(), name='course_list'),
#             path('subject/<slug:subject>/', CourseListView.as_view(), name='course_list_subject'),
#             # path('<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
#             path('module/<int:course_id>/', ModuleListView.as_view(), name='module_list'),
#             path('<pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
#             path('module/<int:module_id>/content/list', ModuleContentListView.as_view(), name='module_content_list'),
#         ], 'courses'), namespace='courses')),
#
#         path('student/', include(([
#             # path('sign_up/', StudentSignUpView.as_view(), name='signup'),
#             path('list/', StudentListView.as_view(), name='list'),
#             path('<slug:slug>/', StudentDetailView.as_view(), name="detail"),
#             path('profile/', ProfileView.as_view(), name='profile'),
#             path('enroll-course/', StudentEnrollCourseView.as_view(), name='student_enroll_course'),
#             path('courses/', StudentCourseListView.as_view(), name='student_course_list'),
#             path('course/<pk>/', StudentCourseDetailView.as_view(), name='student_course_detail'),
#             path('course/<pk>/<module_id>/', StudentCourseDetailView.as_view(), name='student_course_detail_module'),
#                 ], 'students'), namespace='students')),
#
#         path('teacher/', include(([
#                                       path('dashboard/', TeacherDashboard.as_view(), name='dashboard'),
#             path('list/', TeacherListView.as_view(), name='list'),
#             path('<slug:slug>/', TeacherDetailView.as_view(), name='detail'),
#             path('profile/', ProfileView.as_view(), name='profile'),
#             path('courses/', include(([
#                 path('mine/', ManageCourseListView.as_view(), name='manage_course_list'),
#                 path('create/', CourseCreateView.as_view(), name='course_create'),
#                 path('<pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
#                 path('<pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
#                 path('<int:course_id>/module/create/', ModuleCreateUpdateView.as_view(), name='course_module_create'),
#                 path('<slug:course_slug>/module/<slug:module_slug>/', ModuleCreateUpdateView.as_view(), name='course_module_update'),
#                 path('module/<slug:module_slug>/content/<model_name>/create/', ContentCreateUpdateView.as_view(), name='module_content_create'),
#                 path('module/<slug:module_slug>/content/<model_name>/<int:id>/', ContentCreateUpdateView.as_view(), name='module_content_update'),
#                 path('content/<int:id>/delete/', ContentDeleteView.as_view(), name='module_content_delete'),
#                 path('module/<slug:course_slug>/', ModuleListView.as_view(), name='module_list'),
#                 path('module/<slug:module_slug>/content/list', ModuleContentListView.as_view(), name='module_content_list'),
#                 path('module/order/', ModuleOrderView.as_view(), name='module_order'),
#                 path('content/order/', ContentOrderView.as_view(), name='content_order'),
#                 path('subject/<slug:subject>/', CourseListView.as_view(), name='course_list_subject'),
#                 path('<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
#                                           path('<int:course_id>/quiz/create/', QuizCreateUpdateView.as_view(),
#                                                name='quiz_create'),
#                                           path('<int:course_id>/quiz/<int:quiz_id>/edit/',
#                                                QuizCreateUpdateView.as_view(), name='quiz_edit'),
#                                           path('<int:course_id>/quiz/<int:quiz_id>/mcq/create/',
#                                                MCQCreateUpdateView.as_view(), name='mcq_create'),
#                                           path('<int:course_id>/quiz/<int:quiz_id>/mcq/<int:mcq_id>/edit/',
#                                                MCQCreateUpdateView.as_view(), name='mcq_edit'),
#                                           path('<int:course_id>/quizzes/', QuizListView.as_view(), name='quiz_list'),
#                                           path('<int:course_id>/quiz/<int:quiz_id>/mcqs/', MCQListView.as_view(),
#                                                name='mcq_list')
#                 ], 'courses'), namespace='courses')),
#
#             path('student/', include(([
#                path('list/', StudentListView.as_view(), name='list'),
#                # path('add/', TeacherStudentAddView.as_view(), name='add'),
#                path('detail/<int:pk>/', StudentDetailView.as_view(), name="detail"),
#             ], 'students'), namespace='students')),
#         ], 'teachers'), namespace='teachers')) ]
