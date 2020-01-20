from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.mail import send_mail
from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView

from aonebrains_courses.models import OpenCourse
from aonebrains_quiz.models import Quiz
from school_courses.models import SchoolCourse
from school_quiz.models import Quiz as SchoolQuiz
from schools.models import School, Teacher, SchoolStudent
from .forms import CuratorSignUpForm, EditorSignUpForm, UserProfileForm, SuperAdminSignUpForm, StudentSignUpForm, \
    MarketerSignUpForm
from .models import Curator, Editor, SuperAdmin, User, Student, Marketer


class AdminDashboard(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = "accounts/admin_dashboard.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        curators = list(Curator.objects.all())
        editors = list(Editor.objects.all())
        courses = list(OpenCourse.objects.all())
        quizzes = list(Quiz.objects.all())
        school_quizzes = list(SchoolQuiz.objects.all())
        super_admins = list(SuperAdmin.objects.all())
        schools = list(School.objects.all())
        school_teachers = list(Teacher.objects.all())
        school_students = list(SchoolStudent.objects.all())
        school_courses = list(SchoolCourse.objects.all())

        return self.render_to_response({"curators": curators,
                                        "editors": editors,
                                        "courses": courses,
                                        "quizzes": quizzes,
                                        "school_quizzes": school_quizzes,
                                        'super_admins': super_admins,
                                        "schools": schools,
                                        "school_teachers": school_teachers,
                                        "school_students": school_students,
                                        "school_courses": school_courses})


class AllStudentsList(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'accounts/students/list.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request):
        students = list(Student.objects.all()) + list(SchoolStudent.objects.all())
        # school_students = SchoolStudent.objects.all()
        return self.render_to_response({'students': students})


class CuratorDashboard(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = "accounts/curators/dashboard.html"

    def test_func(self):
        return self.request.user.account_type == 'curator'

    def get(self, request, *args, **kwargs):
        courses = list(OpenCourse.objects.filter(creator=request.user.curator))
        quizzes = list(Quiz.objects.filter(course__creator=request.user.curator))

        return self.render_to_response({"courses": courses,
                                        "quizzes": quizzes})


class CuratorListView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    context_object_name = 'curators'
    template_name = 'accounts/curators/list.html'
    curator = None
    form = None

    def test_func(self):
        return self.request.user.account_type == "admin" or self.request.user.account_type == "super admin" or \
               self.request.user.account_type == "editor"

    def get(self, request, *args, **kwargs):
        if request.user.account_type == "super admin":
            self.curator = Curator.objects.filter(admin=request.user.super_admin_profile)
            self.form = CuratorSignUpForm()
        elif request.user.account_type == 'editor':
            self.curator = Curator.objects.filter(admin=request.user.editor.admin)
        elif request.user.account_type == 'admin':
            self.curator = Curator.objects.all()
        return self.render_to_response({'curators': self.curator,
                                        'form': self.form})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        self.form = CuratorSignUpForm(data=request.POST)
        if self.form.is_valid():
            user = self.form.save()
            Curator.objects.get_or_create(user=user, admin=self.request.user.super_admin_profile)
            return redirect('accounts:super_admin:curators:list')
        return self.render_to_response({'form': self.form})


class CuratorDetailView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'accounts/user_detail.html'
    curator = None
    previous_email = None

    def test_func(self):
        return self.request.user.account_type == "super admin" or self.request.user.account_type == "admin"

    def dispatch(self, request, curator_slug, *args, **kwargs):
        if request.user.account_type == 'super admin':
            self.curator = get_object_or_404(Curator,
                                             slug=curator_slug, admin=request.user.super_admin_profile)
        elif request.user.account_type == 'admin':

            self.curator = get_object_or_404(Curator,
                                             slug=curator_slug)
        else:
            raise Http404

        self.previous_email = self.curator.user.email
        return super(CuratorDetailView, self).dispatch(request, curator_slug, *args, **kwargs)

    def get(self, request, curator_slug, *args, **kwargs):
        form = UserProfileForm(instance=self.curator.user)

        return self.render_to_response({'form': form,
                                        'name': self.curator.user.first_name})

    def post(self, request, curator_slug, *args, **kwargs):
        form = UserProfileForm(instance=self.curator.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            if user.email != self.previous_email:
                password = User.objects.make_random_password()
                user.set_password(password)
                print(password)
                send_mail('Account Password', 'UserName: {}\n'
                                              'First Name: {}\n'
                                              'Last Name: {}\n'
                                              'Password for your account is {}'
                                              ''.format(user.username, user.first_name, user.last_name, password),
                          settings.EMAIL_HOST_USER,
                          [user.email])
            user.save()
            return redirect('accounts:curator_list')
        return self.render_to_response({'form': form})


class MarketerDashboard(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = "accounts/marketer/dashboard.html"

    def test_func(self):
        return self.request.user.account_type == 'marketer'

    def get(self, request, *args, **kwargs):
        schools = list(School.objects.filter(marketer=request.user.marketer_profile))
        return self.render_to_response({"schools": schools})


class MarketerListView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'accounts/marketer/list.html'
    marketers = None
    form = None

    def test_func(self):
        return self.request.user.account_type == 'super admin' or self.request.user.account_type == 'admin'

    def get(self, request, superAdmin_slug=None, *args, **kwargs):
        if request.user.account_type == 'super admin':
            self.marketers = Marketer.objects.filter(admin=request.user.super_admin_profile)
            self.form = MarketerSignUpForm()
        elif request.user.account_type == 'admin':
            if superAdmin_slug:
                self.marketers = Marketer.objects.filter(admin__slug=superAdmin_slug)
            else:
                self.marketers = Marketer.objects.all()
        return self.render_to_response({'marketers': self.marketers,
                                        'form': self.form})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        self.form = MarketerSignUpForm(data=request.POST)
        if self.form.is_valid():
            user = self.form.save()
            Marketer.objects.get_or_create(user=user, admin=request.user.super_admin_profile)
            return redirect('accounts:superAdmin_marketers_list')
        return self.render_to_response({'form': self.form})


class MarketerDetailView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'accounts/user_detail.html'
    marketer = None
    previous_email = None

    def test_func(self):
        return self.request.user.account_type == 'super admin' or self.request.user.account_type == 'admin'

    def dispatch(self, request, marketer_slug, *args, **kwargs):
        if request.user.account_type == 'super admin':
            self.marketer = get_object_or_404(Marketer,
                                              slug=marketer_slug, admin=request.user.super_admin_profile)
        elif request.user.account_type == 'admin':
            self.marketer = get_object_or_404(Marketer,
                                              slug=marketer_slug)
        else:
            raise Http404

        self.previous_email = self.marketer.user.email
        return super(MarketerDetailView, self).dispatch(request, marketer_slug, *args, **kwargs)

    def get(self, request, marketer_slug, *args, **kwargs):
        form = UserProfileForm(instance=self.marketer.user)

        return self.render_to_response({'form': form,
                                        'name': self.marketer.user.first_name})

    def post(self, request, marketer_slug, *args, **kwargs):
        form = UserProfileForm(instance=self.marketer.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            if user.email != self.previous_email:
                password = User.objects.make_random_password()
                user.set_password(password)
                print(password)
                send_mail('Account Password', 'UserName: {}\n'
                                              'First Name: {}\n'
                                              'Last Name: {}\n'
                                              'Password for your account is {}'
                                              ''.format(user.username, user.first_name, user.last_name, password),
                          settings.EMAIL_HOST_USER,
                          [user.email])
            user.save()
            if self.request.user.account_type == "super admin":
                return redirect('accounts:superAdmin_marketer_list', self.request.user.super_admin_profile.slug)
            else:
                return reverse_lazy('accounts:marketer_list')
        return self.render_to_response({'form': form})


class EditorDashboard(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = "accounts/editors/dashboard.html"

    def test_func(self):
        return self.request.user.account_type == 'editor'

    def get(self, request):
        courses = list(OpenCourse.objects.filter(creator__admin=request.user.editor.admin))
        curators = list(Curator.objects.filter(admin=request.user.editor.admin))
        quizzes = list(Quiz.objects.filter(course__creator__admin=request.user.editor.admin))
        return self.render_to_response({"courses": courses,
                                        "curators": curators,
                                        "quizzes": quizzes})


class EditorListView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    # context_object_name = 'teachers'
    template_name = 'accounts/editors/list.html'
    editor = None
    form = None

    def test_func(self):
        return self.request.user.account_type == 'super admin' or self.request.user.account_type == 'admin'

    def get(self, request, *args, **kwargs):
        if request.user.account_type == 'super admin':
            self.editor = Editor.objects.filter(admin=request.user.super_admin_profile)
            self.form = EditorSignUpForm()
        elif request.user.account_type == 'admin':
            self.editor = Editor.objects.all()
        return self.render_to_response({'editors': self.editor,
                                        'form': self.form})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        self.form = EditorSignUpForm(data=request.POST, files=request.FILES)
        if self.form.is_valid():
            user = self.form.save()
            Editor.objects.get_or_create(user=user, admin=request.user.super_admin_profile)
            return redirect('accounts:super_admin:editor:list')
        return self.render_to_response({'form': self.form})


class EditorDetailView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'accounts/user_detail.html'
    editor = None
    previous_email = None

    def test_func(self):
        return self.request.user.account_type == 'super admin' or self.request.user.account_type == 'admin'

    def dispatch(self, request, editor_slug, *args, **kwargs):
        if request.user.account_type == 'super admin':
            self.editor = get_object_or_404(Editor,
                                            slug=editor_slug, admin=request.user.super_admin_profile)
        elif request.user.account_type == 'admin':

            self.editor = get_object_or_404(Editor,
                                            slug=editor_slug)
        else:
            raise Http404

        self.previous_email = self.editor.user.email
        return super(EditorDetailView, self).dispatch(request, editor_slug, *args, **kwargs)

    def get(self, request, editor_slug, *args, **kwargs):
        form = UserProfileForm(instance=self.editor.user)

        return self.render_to_response({'form': form,
                                        'name': self.editor.user.first_name})

    def post(self, request, curator_slug, *args, **kwargs):
        form = UserProfileForm(instance=self.editor.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            if user.email != self.previous_email:
                password = User.objects.make_random_password()
                user.set_password(password)
                print(password)
                send_mail('Account Password', 'UserName: {}\n'
                                              'First Name: {}\n'
                                              'Last Name: {}\n'
                                              'Password for your account is {}'
                                              ''.format(user.username, user.first_name, user.last_name, password),
                          settings.EMAIL_HOST_USER,
                          [user.email])
            user.save()
            return redirect('accounts:editor_list')
        return self.render_to_response({'form': form})


class SuperAdminDashboard(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = "accounts/super_admin/dashboard.html"

    def test_func(self):
        return self.request.user.account_type == 'super admin'

    def get(self, request):
        curators = list(Curator.objects.filter(admin=request.user.super_admin_profile))
        editors = list(Editor.objects.filter(admin=request.user.super_admin_profile))
        courses = list(OpenCourse.objects.filter(creator__admin=request.user.super_admin_profile))
        quizzes = list(Quiz.objects.filter(course__creator__admin=request.user.super_admin_profile))
        return self.render_to_response({"curators": curators,
                                        "editors": editors,
                                        "courses": courses,
                                        "quizzes": quizzes})


class StudentDetailView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'accounts/students/detail.html'
    student = None
    school_student = None

    def test_func(self):
        return self.request.user.account_type == 'admin'

    def get(self, request, student_slug):

        try:
            self.student = Student.objects.get(slug=student_slug)
        except Student.DoesNotExist:
            self.student = get_object_or_404(SchoolStudent, slug=student_slug)
        return self.render_to_response({'student': self.student})


class SuperAdminListView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'accounts/super_admin/list.html'
    super_admins = None
    form = None

    def test_func(self):
        return self.request.user.account_type == 'admin'

    def get(self, request, *args, **kwargs):
        self.super_admins = SuperAdmin.objects.all()
        self.form = SuperAdminSignUpForm()
        return self.render_to_response({'super_admins': self.super_admins,
                                        'form': self.form})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        self.form = SuperAdminSignUpForm(data=request.POST)
        if self.form.is_valid():
            user = self.form.save(request=request)
            # send_mail('Account Password', 'Password for your account is {}'.format(self.form.password), self.request.user.email,
            #           [user.email])
            SuperAdmin.objects.get_or_create(user=user)
            return redirect('accounts:super_admin:list')
        return self.render_to_response({'form': self.form})


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        Student.objects.create(user=user)
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('aonebrains_main:profile')  # Redirect url


class ProfileView(TemplateResponseMixin, LoginRequiredMixin, View):
    template_name = 'registration/profile_form.html'
    user_form = None

    def get(self, request, *args, **kwargs):
        self.user_form = UserProfileForm(instance=request.user)
        return self.render_to_response({'form': self.user_form})

    def post(self, request, *args, **kwargs):
        self.user_form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if self.user_form.is_valid():
            self.user_form.save()
            return redirect('accounts:profile')
        return self.render_to_response({'form': self.user_form})


class SuperAdminCuratorsList(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Curator
    template_name = "accounts/curators/list.html"
    context_object_name = "curators"

    def test_func(self):
        return self.request.user.account_type == 'super admin' or self.request.user.account_type == 'admin'

    def get_queryset(self):
        qs = super(SuperAdminCuratorsList, self).get_queryset()
        return qs.filter(admin__slug=self.kwargs['superAdmin_slug'])


class SuperAdminEditorsList(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = Editor
    template_name = "accounts/editors/list.html"
    context_object_name = "editors"

    def test_func(self):
        return self.request.user.account_type == 'super admin' or self.request.user.account_type == 'admin'

    def get_queryset(self):
        qs = super(SuperAdminEditorsList, self).get_queryset()
        return qs.filter(admin__slug=self.kwargs['superAdmin_slug'])


class MarketerSchoolListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = School
    template_name = 'schools/school/list.html'
    context_object_name = 'schools'

    def test_func(self):
        return self.request.user.account_type == 'super admin' or self.request.user.account_type == 'admin'

    def get_queryset(self):
        qs = super(MarketerSchoolListView, self).get_queryset()
        return qs.filter(marketer__slug=self.kwargs['marketer_slug'])


class SuperAdminDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = SuperAdmin
    slug_field = "slug"
    template_name = "accounts/super_admin/detail.html"

    def test_func(self):
        return self.request.user.is_superuser

# class DeactivateCuratorUser(View):
#
#     def post(self, id):
#         if id:
#             user = Curator.objects.get(user=id)
#             user.user.is_active = False
#             user.save()
#             return reverse_lazy('accounts:curator_list')
# #
# class DeactivateCuratorUser(View):
#
#     def post(self, id):
#         if id:
#             user = Curator.objects.get(user=id)
#             user.user.is_active = False
#             user.save()
#             return reverse_lazy('accounts:curator_list')

# class EditorDetailView(DetailView):
#     model = Editor
#     template_name = 'accounts/editors/detail.html'
#     qs = None
#     slug_field = "slug"
#
#     def get_queryset(self):
#         if self.request.user.account_type == 'super admin':
#             self.qs = super(EditorDetailView, self).get_queryset().filter(admin=self.request.user.super_admin_profile)
#         elif self.request.user.account_type == 'admin':
#             self.qs = super(EditorDetailView, self).get_queryset()
#         return self.qs


# class MarketerDetailView(DetailView):
#     model = Marketer
#     template_name = 'accounts/marketer/detail.html'
#     qs = None
#     slug_field = "slug"
#
#     def get_queryset(self):
#         if self.request.user.account_type == 'super admin':
#             self.qs = super(MarketerDetailView, self).get_queryset().filter(admin=self.request.user.super_admin_profile)
#         elif self.request.user.account_type == 'admin':
#             self.qs = super(MarketerDetailView, self).get_queryset()
#         return self.qs

# class CuratorDetailView(DetailView):
#     model = Curator
#     template_name = 'accounts/curators/detail.html'
#     qs = None
#     slug_field = "slug"
#
#     def get_queryset(self):
#         if self.request.user.account_type == 'super admin':
#             self.qs = super(CuratorDetailView, self).get_queryset().filter(admin=self.request.user.super_admin_profile)
#         elif self.request.user.account_type == 'admin':
#             self.qs = super(CuratorDetailView, self).get_queryset()
#         return self.qs
