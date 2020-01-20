from django.urls import path

from school_courses.views import CourseListView, ModuleListView, CourseDeleteView, ModuleContentListView, \
    ManageCourseListView, CourseCreateView, CourseUpdateView, ModuleCreateUpdateView, ContentCreateUpdateView, \
    ContentDeleteView, ModuleOrderView, ContentOrderView, CourseDetailView, SubjectListView

app_name = "school_courses"

urlpatterns = [
    path('mine/', ManageCourseListView.as_view(), name='manage_course_list'),
    path('create/', CourseCreateView.as_view(), name='course_create'),
    path('<pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    path('list/', CourseListView.as_view(), name='course_list'),
    path('subjects/list/', SubjectListView.as_view(), name='subject_list'),
    path('<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    path('<slug:slug>/delete/', CourseDeleteView.as_view(), name='course_delete'),
    path('<int:course_id>/module/create/', ModuleCreateUpdateView.as_view(), name='course_module_create'),
    path('<slug:course_slug>/module/<slug:module_slug>/', ModuleCreateUpdateView.as_view(),
         name='course_module_update'),
    path('<slug:course_slug>/modules/', ModuleListView.as_view(), name='module_list'),
    path('module/<slug:module_slug>/content/<model_name>/create/', ContentCreateUpdateView.as_view(),
         name='module_content_create'),
    path('module/<slug:module_slug>/content/<model_name>/<int:id>/', ContentCreateUpdateView.as_view(),
         name='module_content_update'),
    path('module/<slug:module_slug>/content/list', ModuleContentListView.as_view(), name='module_content_list'),
    path('content/<int:id>/delete/', ContentDeleteView.as_view(), name='module_content_delete'),
    path('module/order/', ModuleOrderView.as_view(), name='module_order'),
    path('content/order/', ContentOrderView.as_view(), name='content_order'),

    # path('subject/<slug:subject>/', CourseListView.as_view(), name='course_list_subject'),
    # path('module/<int:course_id>/', ModuleListView.as_view(), name='module_list'),
    # path('module/<int:module_id>/content/list', ModuleContentListView.as_view(), name='module_content_list'),
    # Teacher
    # path('module/<slug:course_slug>/', ModuleListView.as_view(), name='module_list'),
    # path('subject/<slug:subject>/', CourseListView.as_view(), name='course_list_subject'),
    # path('<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),

]

# School
# path('courses/', include(([
#             path('list/', CourseListView.as_view(), name='course_list'),
#             path('subject/<slug:subject>/', CourseListView.as_view(), name='course_list_subject'),
#             # path('<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
#             path('module/<int:course_id>/', ModuleListView.as_view(), name='module_list'),
#             path('<pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
#             path('module/<int:module_id>/content/list', ModuleContentListView.as_view(), name='module_content_list'),
#         ], 'courses'), namespace='courses')),

# # Teachers
# path('courses/', include(([
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
