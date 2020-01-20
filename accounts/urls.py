from django.contrib.auth.views import PasswordResetView
from django.urls import path, include, reverse_lazy

from aonebrains_courses.views import CourseListView
from schools.views import MarketersSchoolListView
from .views import ProfileView, CuratorListView, EditorListView, CuratorDetailView, EditorDetailView, \
    CuratorDashboard, StudentSignUpView, EditorDashboard, SuperAdminDashboard, AdminDashboard, \
    SuperAdminCuratorsList, SuperAdminEditorsList, AllStudentsList, MarketerListView, MarketerDetailView, \
    MarketerDashboard, StudentDetailView, MarketerSchoolListView, SuperAdminDetailView

app_name = 'accounts'

urlpatterns = [

    # path('', include('registration.backends.admin_approval.urls')),
    path('password_reset/', PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')),
         name='password_reset'),
    path('', include('django.contrib.auth.urls')),
    # path('admin/profile/', ProfileView.as_view(),name='admin_profile'),
    path('sign_up/', StudentSignUpView.as_view(), name="student_sign_up"),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('admin/dashboard/', AdminDashboard.as_view(), name='admin_dashboard'),
    path('students/list/', AllStudentsList.as_view(), name='students_list'),
    path('courses/list/', CourseListView.as_view(), name='course_list'),
    path('curators/list/', CuratorListView.as_view(), name='curator_list'),
    path('curator/dashboard/', CuratorDashboard.as_view(), name='curator_dashboard'),
    path('curator/<slug:curator_slug>/detail/', CuratorDetailView.as_view(), name='curator_detail'),
    # path('curator/deactivate/', DeactivateCuratorUser.as_view(), name='curator_deactivate'),
    path('editors/list/', EditorListView.as_view(), name='editor_list'),
    path('editor/<slug:editor_slug>/detail/', EditorDetailView.as_view(), name='editor_detail'),
    path('editor/dashboard/', EditorDashboard.as_view(), name='editor_dashboard'),
    path('super_admin/dashboard/', SuperAdminDashboard.as_view(), name="super_admin_dashboard"),
    path('super_admin/marketers/list/', MarketerListView.as_view(), name='superAdmin_marketers_list'),
    path('marketers/list/', MarketerListView.as_view(), name='marketer_list'),
    path('marketer/<slug:marketer_slug>/detail/', MarketerDetailView.as_view(), name='marketer_detail'),
    path('<slug:superAdmin_slug>/marketers/list/', MarketerListView.as_view(), name='superAdmin_marketer_list'),
    path('<slug:superAdmin_slug>/curators/list/', SuperAdminCuratorsList.as_view(), name="superAdmin_curators_list"),
    path('<slug:superAdmin_slug>/editors/list/', SuperAdminEditorsList.as_view(), name="superAdmin_editors_list"),
    path('marketer/schools/list/', MarketersSchoolListView.as_view(), name='marketer_school_list'),
    path('marketer/<slug:marketer_slug>/schools/list/', MarketerSchoolListView.as_view(), name='marketer_schools'),
    path('marketer/dashboard/', MarketerDashboard.as_view(), name='marketer_dashboard'),
    path('student/<slug:student_slug>/detail/', StudentDetailView.as_view(), name='student_detail'),
    path('super_admin/<slug:slug>/detail/', SuperAdminDetailView.as_view(), name="super_admin_detail"),

    # path('super_admin/', include(([
    #                                   path('list/', SuperAdminListView.as_view(), name='list'),
    #                                   path('profile/', ProfileView.as_view(), name='profile'),
    #                                   path('curators/', include(([
    #                                                                  path('dashboard/', CuratorDashboard.as_view(),
    #                                                                       name='dashboard'),
    #                                                                  path('list/', CuratorListView.as_view(),
    #                                                                       name='list'),
    #                                                                  path('<pk>/detail/', CuratorDetailView.as_view(),
    #                                                                       name='detail'),
    #                                                                  path('profile/', ProfileView.as_view(),
    #                                                                       name='profile'),
    #                                                                  path('courses/', include(([
    #                                                                                                path('mine/',
    #                                                                                                     ManageCourseListView.as_view(),
    #                                                                                                     name='manage_course_list'),
    #                                                                                                path('create/',
    #                                                                                                     CourseCreateView.as_view(),
    #                                                                                                     name='course_create'),
    #                                                                                                path('<pk>/edit/',
    #                                                                                                     CourseUpdateView.as_view(),
    #                                                                                                     name='course_edit'),
    #                                                                                                path('<pk>/delete/',
    #                                                                                                     CourseDeleteView.as_view(),
    #                                                                                                     name='course_delete'),
    #                                                                                                path(
    #                                                                                                    '<int:course_id>/module/create/',
    #                                                                                                    ModuleCreateUpdateView.as_view(),
    #                                                                                                    name='course_module_create'),
    #                                                                                                path(
    #                                                                                                    '<int:course_id>/module/<int:module_id>/',
    #                                                                                                    ModuleCreateUpdateView.as_view(),
    #                                                                                                    name='course_module_update'),
    #                                                                                                path(
    #                                                                                                    'module/<int:module_id>/content/<model_name>/create/',
    #                                                                                                    ContentCreateUpdateView.as_view(),
    #                                                                                                    name='module_content_create'),
    #                                                                                                path(
    #                                                                                                    'module/<int:module_id>/content/<model_name>/<int:id>/',
    #                                                                                                    ContentCreateUpdateView.as_view(),
    #                                                                                                    name='module_content_update'),
    #                                                                                                path(
    #                                                                                                    'content/<int:id>/delete/',
    #                                                                                                    ContentDeleteView.as_view(),
    #                                                                                                    name='module_content_delete'),
    #                                                                                                path(
    #                                                                                                    'module/<int:course_id>/',
    #                                                                                                    ModuleListView.as_view(),
    #                                                                                                    name='module_list'),
    #                                                                                                path(
    #                                                                                                    'module/<int:module_id>/content/list',
    #                                                                                                    ModuleContentListView.as_view(),
    #                                                                                                    name='module_content_list'),
    #                                                                                                path('module/order/',
    #                                                                                                     ModuleOrderView.as_view(),
    #                                                                                                     name='module_order'),
    #                                                                                                path(
    #                                                                                                    'content/order/',
    #                                                                                                    ContentOrderView.as_view(),
    #                                                                                                    name='content_order'),
    #                                                                                                path(
    #                                                                                                    'subject/<slug:subject>/',
    #                                                                                                    CourseListView.as_view(),
    #                                                                                                    name='course_list_subject'),
    #                                                                                                # path('<slug:slug>/',
    #                                                                                                #      CourseDetailView.as_view(),
    #                                                                                                #      name='course_detail'),
    #                                                                                                path(
    #                                                                                                    '<int:course_id>/quiz/create/',
    #                                                                                                    QuizCreateUpdateView.as_view(),
    #                                                                                                    name='quiz_create'),
    #                                                                                                path(
    #                                                                                                    '<int:course_id>/quiz/<int:quiz_id>/edit/',
    #                                                                                                    QuizCreateUpdateView.as_view(),
    #                                                                                                    name='quiz_edit'),
    #                                                                                                path(
    #                                                                                                    '<int:course_id>/quiz/<int:quiz_id>/mcq/create/',
    #                                                                                                    MCQCreateUpdateView.as_view(),
    #                                                                                                    name='mcq_create'),
    #                                                                                                path(
    #                                                                                                    '<int:course_id>/quiz/<int:quiz_id>/mcq/<int:mcq_id>/edit/',
    #                                                                                                    MCQCreateUpdateView.as_view(),
    #                                                                                                    name='mcq_edit'),
    #                                                                                                path(
    #                                                                                                    '<int:course_id>/quizzes/',
    #                                                                                                    QuizListView.as_view(),
    #                                                                                                    name='quiz_list'),
    #                                                                                                path(
    #                                                                                                    '<int:course_id>/quiz/<int:quiz_id>/mcqs/',
    #                                                                                                    MCQListView.as_view(),
    #                                                                                                    name='mcq_list')
    #                                                                                            ], 'courses'),
    #                                                                      namespace='courses')),
    #                                                              ], 'curators'), namespace='curator')),
    #
    #                                   path('editors/', include(([
    #                                                                 path('list/', EditorListView.as_view(),
    #                                                                      name='list'),
    #                                                                 path('profile/', ProfileView.as_view(),
    #                                                                      name='profile'),
    #                                                                 path('<pk>/detail/', EditorDetailView.as_view(),
    #                                                                      name='detail'),
    #                                                                 path('courses/', include(([
    #                                                                                               path('list/',
    #                                                                                                    CourseListView.as_view(),
    #                                                                                                    name='course_list'),
    #                                                                                           ], 'courses'),
    #                                                                     namespace='courses')),
    #                                                                 path('curators/', include(([
    #                                                                                                path('list/',
    #                                                                                                     CuratorListView.as_view(),
    #                                                                                                     name='list'),
    #                                                                                                path('courses/',
    #                                                                                                     include(([
    #                                                                                                                  path(
    #                                                                                                                      '<int:curator_id>/list/',
    #                                                                                                                      CuratorCoursesListView.as_view(),
    #                                                                                                                      name='course_list'),
    #                                                                                                              ],
    #                                                                                                              'courses'),
    #                                                                                                         namespace='courses')),
    #                                                                                            ], 'curators'),
    #                                                                     namespace='curator')),
    #                                                             ], 'editor'), namespace='editor')),
    #
    #                                   path('courses/', include(([
    #                                                                 path('list/', CourseListView.as_view(),
    #                                                                      name='course_list'),
    #                                                                 path('subject/<slug:subject>/',
    #                                                                      CourseListView.as_view(),
    #                                                                      name='course_list_subject'),
    #                                                                 # path('<slug:slug>/', CourseDetailView.as_view(), name='course_detail'),
    #                                                                 path('module/<int:course_id>/',
    #                                                                      ModuleListView.as_view(), name='module_list'),
    #                                                                 path('<int:curator_id>/delete/',
    #                                                                      CourseDeleteView.as_view(),
    #                                                                      name='course_delete'),
    #                                                                 path('module/<int:module_id>/content/list',
    #                                                                      ModuleContentListView.as_view(),
    #                                                                      name='module_content_list'),
    #                                                             ], 'courses'), namespace='courses')),
    #
    #                               ], 'super_admin'), namespace='super_admin'))
]
