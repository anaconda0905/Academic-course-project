from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.list import ListView
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get

from accounts.forms import UserProfileForm
from accounts.models import User, Student
from school_courses.forms import CourseEnrollForm
from school_courses.models import SchoolCourse
from school_quiz.models import Quiz
from schools.tasks import register_students
from .forms import StudentSignUpForm, SchoolSignUpForm, SchoolUserForm, SchoolProfileForm, TeacherSignUpForm, \
    TeacherStudentForm, TeacherClassForm, MarketerSchoolSignUpForm
from .models import Teacher, SchoolStudent, School


class SchoolSignUpView(CreateView):
    model = User
    form_class = SchoolSignUpForm
    template_name = 'schools/registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'School'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        School.objects.create(user=user)
        login(self.request, user)
        return redirect('schools:profile')  # Redirect url


class SchoolListView(UserPassesTestMixin, LoginRequiredMixin, ListView):

    def test_func(self):
        return self.request.user.account_type == "admin"

    model = School
    template_name = "schools/school/list.html"
    context_object_name = 'schools'


class MarketersSchoolListView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    context_object_name = 'schools'
    template_name = 'schools/school/list.html'
    form = None
    school = None

    def test_func(self):
        return self.request.user.account_type == "admin" or self.request.user.account_type == "marketer"

    def get(self, request):
        if self.request.user.account_type == "marketer":
            self.school = School.objects.filter(marketer=request.user.marketer_profile)
            self.form = MarketerSchoolSignUpForm()
        elif self.request.user.account_type == "admin":
            self.school = School.objects.filter(marketer__slug=self.kwargs['marketer_slug'])
        return self.render_to_response({'schools': self.school,
                                        'form': self.form})

    @transaction.atomic
    def post(self, request):
        if self.request.user.account_type == "marketer":
            self.form = MarketerSchoolSignUpForm(data=request.POST)
            if self.form.is_valid():
                user = self.form.save()
                exist, created = School.objects.get_or_create(user=user, marketer=self.request.user.marketer_profile)
                if exist and exist.marketer == 'null':
                    exist.marketer = self.request.user.marketer_profile
                return redirect('accounts:marketer_school_list')
        return self.render_to_response({'form': self.form})


class SchoolDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = School
    template_name = "schools/school/detail.html"
    context_object_name = 'school'
    slug_field = 'slug'

    def test_func(self):
        return self.request.user.account_type == "admin"

    # def get_object(self, queryset=None):
    #     return get_object_or_404(School, name=self.kwargs['name'])


# class StudentSignUpView(CreateView):
#     model = User
#     form_class = StudentSignUpForm
#     context_object_name = 'form'
#     template_name = 'schools/student/list.html'
#
#     def get_context_data(self, **kwargs):
#         kwargs['user_type'] = 'SchoolStudent'
#         return super().get_context_data(**kwargs)
#
#     @transaction.atomic
#     def form_valid(self, form):
#         user = form.save()
#         SchoolStudent.objects.get_or_create(user=user, school=self.request.user.school_profile)
#         return redirect('accounts:dashboard')


# class TeacherSignUpView(TemplateResponseMixin, View):
#     template_name = 'schools/registration/signup_form.html'
#
#     def get(self, request, *args, **kwargs):
#         tea_form = TeacherSignUpForm()
#         tea_class_form = TeacherClassForm()
#         return self.render_to_response({'form': tea_form,
#                                         'class_form':tea_class_form,
#                                         'user_type':'Teacher'})
#
#     @transaction.atomic
#     def post(self, request, *args, **kwargs):
#         tea_form = TeacherSignUpForm(data=request.POST)
#         tea_class_form = TeacherClassForm(data=request.POST)
#         if tea_form.is_valid() and tea_class_form.is_valid():
#             user = tea_form.save()
#             grade = tea_class_form.cleaned_data['grade']
#             Teacher.objects.get_or_create(user=user, school=self.request.user.school_profile, grade=grade)
#             return redirect("accounts:dashboard")
#         return self.render_to_response({'form': tea_form,
#                                         'class_form': tea_class_form,
#                                         'user_type':'Teacher'})


class TeacherListView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    context_object_name = 'teachers'
    template_name = 'schools/school/teacher_list.html'
    teacher = None
    form = None
    class_form = None

    def test_func(self):
        return self.request.user.account_type == "admin" or \
               self.request.user.account_type == "school"

    def get(self, request, *args, **kwargs):
        if self.request.user.account_type == "school":
            self.teacher = Teacher.objects.filter(school=request.user.school_profile)
            self.form = TeacherSignUpForm()
            self.class_form = TeacherClassForm()
        elif self.request.user.account_type == "admin":
            self.teacher = Teacher.objects.filter(school__slug=self.kwargs['school_slug'])
        return self.render_to_response({'teachers': self.teacher,
                                        'class_form': self.class_form,
                                        'form': self.form})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if self.request.user.account_type == "school":
            self.form = TeacherSignUpForm(data=request.POST, files=request.FILES)
            self.class_form = TeacherClassForm(data=request.POST)
            if self.form.is_valid() and self.class_form.is_valid():
                user = self.form.save(self, request=request)
                grade = self.class_form.cleaned_data['grade']
                Teacher.objects.get_or_create(user=user, school=self.request.user.school_profile, grade=grade)
                return redirect('schools:teachers:list')
        return self.render_to_response({'form': self.form,
                                        'class_form': self.class_form})


# class TeacherStudentAddView(FormView):
#     template_name = 'schools/teacher/student_add.html'
#     form_class = TeacherStudentForm
#
#     def form_valid(self, form):
#         username = form.cleaned_data['username']
#         student = get_object_or_404(SchoolStudent,
#                                     user__username=username)
#         student.teacher.add(self.request.user.teacher_profile)
#         return HttpResponse("DONNNNNNNNEEEEEEEEE!!!!!!!!!!!!!")


class StudentListView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    # context_object_name = 'students'
    template_name = 'schools/student/list.html'
    students = None
    form = None

    def get(self, request, *args, **kwargs):
        if request.user.account_type == "school":
            self.students = SchoolStudent.objects.filter(school=request.user.school_profile)
            self.form = StudentSignUpForm()
        elif request.user.account_type == 'teacher':
            self.students = SchoolStudent.objects.filter(teacher=request.user.teacher_profile,
                                                         school=request.user.teacher_profile.school)
            self.form = TeacherStudentForm()
        elif request.user.account_type == 'admin':
            self.students = SchoolStudent.objects.filter(school__slug=self.kwargs['school_slug'])
        elif request.user.account_type == 'marketer':
            self.students = SchoolStudent.objects.filter(school__slug=self.kwargs['school_slug'],
                                                         school__marketer=request.user.marketer_profile)
        return self.render_to_response({'students': self.students,
                                        'form': self.form})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if request.user.account_type == "school":
            self.form = StudentSignUpForm(data=request.POST, files=request.FILES)
            if self.form.is_valid():
                user = self.form.save(self, request=request)
                SchoolStudent.objects.get_or_create(user=user, school=self.request.user.school_profile)
                Student.objects.get_or_create(user=user)
                return redirect('schools:students:list')
        elif request.user.account_type == 'teacher':
            self.form = TeacherStudentForm(data=request.POST)
            if self.form.is_valid():
                username = self.form.cleaned_data['username']
                student = get_object_or_404(SchoolStudent,
                                            user__username=username, school=request.user.teacher_profile.school)
                student.teacher.add(self.request.user.teacher_profile)
                return redirect('schools:teachers:students:list')
        return self.render_to_response({'form': self.form})


class ProfileView(TemplateResponseMixin, View):
    template_name = 'schools/registration/profile_form.html'
    user_form = None
    profile_form = None

    def get(self, request, *args, **kwargs):
        if request.user.account_type == 'school':
            self.user_form = SchoolUserForm(instance=request.user)
            self.profile_form = SchoolProfileForm(instance=request.user.school_profile)
        elif request.user.account_type == 'teacher' or request.user.account_type == 'student':
            self.user_form = UserProfileForm(instance=request.user)
        return self.render_to_response({'form': self.user_form,
                                        'profile_form': self.profile_form})

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        if request.user.account_type == 'school' or request.user.is_school:
            self.user_form = SchoolUserForm(instance=request.user, data=request.POST, files=request.FILES)
            self.profile_form = SchoolProfileForm(instance=request.user.school_profile, data=request.POST)
            if self.user_form.is_valid() and self.profile_form.is_valid():
                self.user_form.save()
                self.profile_form.save()
                return redirect('schools:profile')
        elif request.user.account_type == 'teacher' or request.user.account_type == 'student':
            self.user_form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
            print(request.POST)
            if self.user_form.is_valid():
                self.user_form.save()
                return redirect('schools:teachers:profile')
        return self.render_to_response({'form': self.user_form,
                                        'profile_form': self.profile_form})


class TeacherDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = Teacher
    template_name = 'schools/teacher/detail.html'
    qs = None

    def test_func(self):
        return self.request.user.account_type == "admin" or \
               self.request.user.account_type == "school"

    def get_queryset(self):
        if self.request.user.account_type == "school":
            qs = super(TeacherDetailView, self).get_queryset().filter(school=self.request.user.school_profile)
        elif self.request.user.account_type == "admin":
            qs = super(TeacherDetailView, self).get_queryset()
        return qs


class StudentDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = SchoolStudent
    template_name = 'schools/student/detail.html'
    context_object_name = 'student'

    def test_func(self):
        return self.request.user.account_type == "admin" or self.request.user.account_type == "teacher" or \
               self.request.user.account_type == "school"

    def get_queryset(self):
        if self.request.user.account_type == 'school':
            qs = super(StudentDetailView, self).get_queryset().filter(school=self.request.user.school_profile)
        elif self.request.user.account_type == 'teacher':
            qs = super(StudentDetailView, self).get_queryset().filter(teacher=self.request.user.teacher_profile,
                                                                      school=self.request.user.teacher_profile.school)
        elif self.request.user.account_type == "admin":
            qs = super(StudentDetailView, self).get_queryset()
            return qs


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail',
                            args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = SchoolCourse
    template_name = 'schools/student/course/list.html'

    def get_queryset(self):
        qs = super(StudentCourseListView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(DetailView):
    model = SchoolCourse
    template_name = 'schools/student/course/detail.html'

    def get_queryset(self):
        qs = super(StudentCourseDetailView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(StudentCourseDetailView, self).get_context_data(**kwargs)

        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(
                id=self.kwargs['module_id'])
        else:
            # get first module
            context['module'] = course.modules.all()[0]
        return context


class SchoolDashboard(TemplateResponseMixin, View):
    template_name = "schools/school/dashboard.html"

    def get(self, request, *args, **kwargs):
        school = request.user.school_profile
        teachers = list(Teacher.objects.filter(school=school))
        students = list(SchoolStudent.objects.filter(school=school))
        courses = list(SchoolCourse.objects.filter(school=school))
        quizzes = list(Quiz.objects.filter(course__school=school))
        return self.render_to_response({'teachers': teachers,
                                        'students': students,
                                        'courses': courses,
                                        'quizzes': quizzes})


class TeacherDashboard(TemplateResponseMixin, View):
    template_name = "schools/teacher/dashboard.html"

    def get(self, request, *args, **kwargs):
        teacher = request.user.teacher_profile
        students = list(SchoolStudent.objects.filter(teacher=teacher))
        courses = list(SchoolCourse.objects.filter(creator=teacher))
        quizzes = list(Quiz.objects.filter(course__creator=teacher))
        return self.render_to_response({'students': students,
                                        'courses': courses,
                                        'quizzes': quizzes})


class SchoolStudentsList(ListView):
    model = SchoolStudent
    template_name = ''

    def get_queryset(self):
        qs = super(SchoolStudentsList, self).get_queryset()
        return qs.filter(school=self.kwargs['school_slug'])


class SchoolTeacherList(ListView):
    model = Teacher
    template_name = ''

    def get_queryset(self):
        qs = super(SchoolTeacherList, self).get_queryset()
        return qs.filter(school=self.kwargs['school_slug'])


class RegisterMultipleStudentsParseExcel(UserPassesTestMixin, LoginRequiredMixin, View):

    def test_func(self):
        return self.request.user.account_type == "school"

    def post(self, request, format=None):
        try:
            excel_file = request.FILES['fileToUpload']
        except MultiValueDictKeyError:
            # return reverse_lazy("schools:students:list")
            return HttpResponse("No File")

        if str(excel_file).split('.')[-1] == 'xls':
            data = xls_get(excel_file, column_limit=6)
        elif str(excel_file).split('.')[-1] == 'xlsx':
            data = xlsx_get(excel_file, column_limit=6)
        else:
            return HttpResponse("Error of Invalid file")
        students = data["Students"]

        register_students.delay(request.user, students)

        return redirect("schools:students:list")

# class RegisterMultipleTeachersParseExcel(View):
#
#     def post(self, request, format=None):
#         try:
#             excel_file = request.FILES['fileToUpload']
#         except MultiValueDictKeyError:
#             # return reverse_lazy("schools:students:list")
#             return HttpResponse("No File")
#         if str(excel_file).split('.')[-1] == 'xls':
#             data = xls_get(excel_file, column_limit=7)
#         elif str(excel_file).split('.')[-1] == 'xlsx':
#             data = xlsx_get(excel_file, column_limit=7)
#         else:
#             return HttpResponse("Error of Invalid file")
#         teachers = data["Teachers"]
#
#         register_teachers.delay(request.user, teachers)
#
#         return redirect("schools:teachers:list")
