from django.urls import path

from .views import CuratorCoursesListView, ModuleListView, CourseDeleteView, ModuleContentListView, \
    ModuleCreateUpdateView, CuratorCourseDetailView, CuratorCourseModuleDetailView, CourseUpdateView, \
    ManageCourseListView, ContentCreateUpdateView, ContentDeleteView, CourseListView, SubjectListView, ClassListView, \
    GradeCoursesListView, GradeDeleteView, SubjectDeleteView, SubjectCourseListView, ContentDetailView, \
    CourseCreateView, SubjectEditView, ModuleDeleteView

app_name = 'aonebrains_courses'

urlpatterns = [
    path('class/<slug:grade_slug>/courses/list/,', GradeCoursesListView.as_view(), name='class_courses_list'),
    path('class/<slug:slug>/delete/', GradeDeleteView.as_view(), name="grade_delete"),
    path('subject/<slug:slug>/delete/', SubjectDeleteView.as_view(), name="subject_delete"),
    path('subject/<slug:slug>/edit/', SubjectEditView.as_view(), name="subject_edit"),
    path('subject/<slug:subject_slug>/courses/list/', SubjectCourseListView.as_view(), name='subject_course_list'),
    path('subjects/list/', SubjectListView.as_view(), name='subject_list'),
    path('classes/list/', ClassListView.as_view(), name='class_list'),
    path('<slug:curator_slug>/course/list/', CuratorCoursesListView.as_view(), name='curator_course_list'),
    path('list/', CourseListView.as_view(), name='course_list'),
    path('<slug:course_slug>/module/create/', ModuleCreateUpdateView.as_view(), name='curator_course_module_create'),
    path('<slug:course_slug>/module/<slug:module_slug>/', ModuleCreateUpdateView.as_view(),
         name='curator_course_module_update'),
    path('mine/', ManageCourseListView.as_view(), name='curator_courses'),
    path('create/', CourseCreateView.as_view(),
         name='course_create'),
    path('<slug:slug>/details/', CuratorCourseDetailView.as_view(), name='course_detail'),
    path('module/<slug:slug>/delete/', ModuleDeleteView.as_view(), name='module_delete'),
    path('module/<slug:slug>/details/', CuratorCourseModuleDetailView.as_view(), name='course_module_detail'),
    path('<slug:slug>/edit/', CourseUpdateView.as_view(), name='curator_course_edit'),
    path('module/<slug:course_slug>/list/', ModuleListView.as_view(), name='curator_course_module_list'),
    path('<slug:slug>/delete/', CourseDeleteView.as_view(), name='curator_course_delete'),
    path('module/<slug:module_slug>/content/list', ModuleContentListView.as_view(), name='module_content_list'),
    path('module/<slug:module_slug>/content/<model_name>/create/', ContentCreateUpdateView.as_view(),
         name='curator_module_content_create'),
    path('module/<slug:module_slug>/content/<model_name>/<int:id>/', ContentCreateUpdateView.as_view(),
         name='curator_module_content_update'),
    path('content/<int:id>/delete/', ContentDeleteView.as_view(), name='curator_module_content_delete'),
    path('content/<int:pk>/detail/', ContentDetailView.as_view(), name='curator_module_content_detail'),

]
