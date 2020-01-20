from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, redirect
# Create your views here.
from django.views.generic import ListView
from django.views.generic.base import View, TemplateResponseMixin

from accounts.forms import UserProfileForm
from accounts.models import Curator, Student
from aonebrains_courses.models import OpenCourse, OpenSubject
from aonebrains_main.forms import CourseEnrollForm, SchoolCourseEnrollForm
from school_courses.models import SchoolSubject, SchoolCourse
from schools.models import School, SchoolStudent


class Home(TemplateResponseMixin, View):
    template_name = "aonebrains_main/home.html"

    def get(self, request):
        courses = OpenCourse.objects.filter(draft=False, approved=True).order_by('-created')[:3]
        total_schools = School.objects.count()
        total_students = SchoolStudent.objects.count() + Student.objects.count()
        total_courses = OpenCourse.objects.count()
        total_curators = Curator.objects.count()
        return self.render_to_response({"courses": courses,
                                        "total_schools": total_schools,
                                        "total_students": total_students,
                                        "total_courses": total_courses,
                                        "total_curators": total_curators})


class AllCoursesListView(TemplateResponseMixin, View):
    template_name = "aonebrains_main/courses/list.html"

    def get(self, request):
        subjects = OpenSubject.objects.all()
        courses_list = OpenCourse.objects.filter(draft=False, approved=True).order_by('-created')
        page = request.GET.get('page', 1)
        paginator = Paginator(courses_list, 6)
        try:
            courses = paginator.page(page)
        except PageNotAnInteger:
            courses = paginator.page(1)
        except EmptyPage:
            courses = paginator.page(paginator.num_pages)

        return self.render_to_response({"courses": courses,
                                        'subjects': subjects,
                                        'course_pag': courses})


class CourseDetailView(TemplateResponseMixin, View):
    template_name = 'aonebrains_main/courses/detail.html'
    course = None
    related_class_courses = None
    latest_courses = None
    enrollment_course = None

    def get(self, request, course_slug):
        self.course = get_object_or_404(OpenCourse, draft=False, slug=course_slug, approved=True)
        self.related_class_courses = OpenCourse.objects.filter(draft=False, grade=self.course.grade, approved=True)
        self.latest_courses = OpenCourse.objects.all().order_by('-created')[:5]
        enroll_course = CourseEnrollForm()
        return self.render_to_response({"enroll_course": enroll_course,
                                        "opencourse": self.course,
                                        "related_class_courses": self.related_class_courses,
                                        "latest_courses": self.latest_courses})

    def post(self, request, course_slug):
        form_class = CourseEnrollForm(data=request.POST)
        if form_class.is_valid():
            self.enrollment_course = form_class.cleaned_data['course']
            self.enrollment_course.students.add(self.request.user.open_student_profile)
            return redirect('aonebrains_main:student_course_detail',
                            self.enrollment_course.slug)
        return self.render_to_response({"enroll_course": form_class})


# class StudentEnrollCourseView(LoginRequiredMixin, FormView):
#     course = None
#     form_class = CourseEnrollForm
#
#     def form_valid(self, form):
#         self.course = form.cleaned_data['course']
#         self.course.students.add(self.request.user.open_student_profile)
#         return super(StudentEnrollCourseView,
#                      self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('aonebrains_main:course_detail',
#                             args=[self.course.slug])
#

# class StudentEnrollCourseView(View):
#     course = None
#     form = None
#
#     def post(self, request):
#         self.form = CourseEnrollForm(request.POST)
#         # if self.form.is_valid():
#         #     print("asdsad")
#         self.course = self.form.cleaned_data['course']
#         self.course.students.add(self.request.user.open_student_profile)
#         print("sadasdad")
#         return reverse_lazy('aonebrains_main:Home')
#         # return HttpResponse(status=200)


class StudentCourseDetailView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'aonebrains_main/students/courses/detail.html'
    course = None
    related_class_courses = None
    latest_courses = None
    quizzes = None

    def test_func(self):
        return self.request.user.account_type == "aonestudent" or self.request.user.account_type == "student"

    def get(self, request, course_slug):
        self.course = get_object_or_404(OpenCourse,
                                        draft=False,
                                        slug=course_slug,
                                        approved=True,
                                        students__in=[self.request.user.open_student_profile])
        self.related_class_courses = OpenCourse.objects.filter(grade=self.course.grade)
        self.latest_courses = OpenCourse.objects.all().order_by('-created')[:5]
        self.quizzes = self.course.quiz_set.all()
        return self.render_to_response({'quizzes': self.quizzes,
                                        "opencourse": self.course,
                                        "related_class_courses": self.related_class_courses,
                                        "latest_courses": self.latest_courses})


class StudentCourseListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = OpenCourse
    template_name = 'aonebrains_main/students/courses/list.html'
    paginate_by = 6
    context_object_name = "courses"

    def test_func(self):
        return self.request.user.account_type == "aonestudent" or self.request.user.account_type == "student"

    def get_queryset(self):
        qs = super(StudentCourseListView, self).get_queryset()
        return qs.filter(students__in=[self.request.user.open_student_profile])

    def get_context_data(self, object_list=None, **kwargs):
        context = super(StudentCourseListView, self).get_context_data()
        context['subjects'] = OpenSubject.objects.all()
        return context


class SchoolCoursesListView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = "aonebrains_main/schools/courses/list.html"

    def test_func(self):
        return self.request.user.account_type == "student"

    def get(self, request):
        subjects = SchoolSubject.objects.all()
        courses_list = SchoolCourse.objects.filter(draft=False, school=request.user.school_student_profile.school)
        page = request.GET.get('page', 1)
        paginator = Paginator(courses_list, 6)
        try:
            courses = paginator.page(page)
        except PageNotAnInteger:
            courses = paginator.page(1)
        except EmptyPage:
            courses = paginator.page(paginator.num_pages)

        return self.render_to_response({"courses": courses,
                                        'subjects': subjects,
                                        'course_pag': courses,
                                        'school_label': "School Courses"})


class SchoolCourseDetailView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'aonebrains_main/schools/courses/detail.html'
    course = None
    related_class_courses = None
    latest_courses = None
    enrollment_course = None

    def test_func(self):
        return self.request.user.account_type == "student"

    def get(self, request, course_slug):
        self.course = get_object_or_404(SchoolCourse, slug=course_slug)
        self.related_class_courses = SchoolCourse.objects.filter(
                                                                 grade=self.course.grade,
                                                                 school=request.user.school_student_profile.school)
        self.latest_courses = SchoolCourse.objects.filter(
                                                          school=request.user.school_student_profile.school).order_by(
            '-created')[:5]
        enroll_course = SchoolCourseEnrollForm()
        return self.render_to_response({"enroll_course": enroll_course,
                                        "opencourse": self.course,
                                        "related_class_courses": self.related_class_courses,
                                        "latest_courses": self.latest_courses})

    def post(self, request, course_slug):
        form_class = SchoolCourseEnrollForm(data=request.POST)
        if form_class.is_valid():
            self.enrollment_course = form_class.cleaned_data['course']
            self.enrollment_course.students.add(self.request.user.school_student_profile)
            return redirect('aonebrains_main:school_student_course_detail',
                            self.enrollment_course.slug)
        return self.render_to_response({"enroll_course": form_class})


class SchoolStudentCourseListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    model = SchoolCourse
    template_name = 'aonebrains_main/schools/students/courses/list.html'
    paginate_by = 6
    context_object_name = "courses"

    def test_func(self):
        return self.request.user.account_type == "student"

    def get_queryset(self):
        qs = super(SchoolStudentCourseListView, self).get_queryset()
        return qs.filter(students__in=[self.request.user.school_student_profile],
                         school=self.request.user.school_student_profile)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SchoolStudentCourseListView, self).get_context_data()
        context['subjects'] = SchoolSubject.objects.all()
        return context


class SchoolStudentCourseDetailView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'aonebrains_main/schools/students/courses/detail.html'
    course = None
    related_class_courses = None
    latest_courses = None
    quizzes = None

    def test_func(self):
        return self.request.user.account_type == "student"

    def get(self, request, course_slug):
        self.course = get_object_or_404(SchoolCourse,

                                        slug=course_slug,
                                        students__in=[self.request.user.school_student_profile])
        self.related_class_courses = SchoolCourse.objects.filter(
                                                                 grade=self.course.grade,
                                                                 school=self.request.user.school_student_profile.school)
        self.latest_courses = SchoolCourse.objects.filter(
            draft=False,
            school=self.request.user.school_student_profile.school).order_by('-created')[:5]
        self.quizzes = self.course.quiz_set.all()
        return self.render_to_response({'quizzes': self.quizzes,
                                        "opencourse": self.course,
                                        "related_class_courses": self.related_class_courses,
                                        "latest_courses": self.latest_courses})


# class CourseDetailView(TemplateResponseMixin, View):
#     template_name = "aonebrains_main/courses/detail.html"
#     course = None
#     related_class_courses = None
#     latest_courses = None
#
#     def get(self, request, course_slug):
#         self.course = get_object_or_404(OpenCourse,
#                                         slug=course_slug)
#         self.related_class_courses = OpenCourse.objects.filter(grade=self.course.grade)
#         self.latest_courses = OpenCourse.objects.all().order_by('-created')[:5]
#         return self.render_to_response({"opencourse": self.course,
#                                         "related_class_courses": self.related_class_courses,
#                                         "latest_courses": self.latest_courses})

class ProfileView(TemplateResponseMixin, LoginRequiredMixin, View):
    template_name = 'aonebrains_main/students/profile_form.html'
    user_form = None

    def get(self, request, *args, **kwargs):
        self.user_form = UserProfileForm(instance=request.user)
        return self.render_to_response({'form': self.user_form})

    def post(self, request, *args, **kwargs):
        self.user_form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if self.user_form.is_valid():
            self.user_form.save()
            return redirect('aonebrains_main:Home')
        return self.render_to_response({'form': self.user_form})
