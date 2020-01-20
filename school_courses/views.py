from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.forms.models import modelform_factory
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .forms import CourseEnrollForm, ModuleCreateForm
from .models import SchoolCourse, SchoolModule, SchoolContent, SchoolSubject


class OwnerMixin(UserPassesTestMixin, object):

    def test_func(self):
        return self.request.user.account_type == "admin" or self.request.user.account_type == "teacher" or \
               self.request.user.account_type == "school"

    def get_queryset(self):
        if self.request.user.account_type == 'teacher':
            qs = super(OwnerMixin, self).get_queryset()
            return qs.filter(creator=self.request.user.teacher_profile)
        elif self.request.user.account_type == 'admin':
            qs = super(OwnerMixin, self).get_queryset()
            return qs
        elif self.request.user.account_type == 'school':
            qs = super(OwnerMixin, self).get_queryset()
            return qs.filter(creator__school=self.request.user.school_profile)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.creator = self.request.user.teacher_profile
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin):
    model = SchoolCourse
    fields = ['subject', 'title', 'overview']
    success_url = reverse_lazy('schools:teachers:courses:manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['preview', 'subject', 'title', 'overview']
    success_url = reverse_lazy('schools:teachers:courses:manage_course_list')
    template_name = 'school_courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'school_courses/manage/course/list.html'


class CourseCreateView(LoginRequiredMixin, OwnerCourseEditMixin, CreateView):

    def form_valid(self, form):
        SchoolCourse.objects.get_or_create(title=form.cleaned_data['title'],
                                           subject=form.cleaned_data['subject'],
                                           overview=form.cleaned_data['overview'],
                                           creator=self.request.user.teacher_profile,
                                           school=self.request.user.teacher_profile.school,
                                           grade=self.request.user.teacher_profile.grade)
        return redirect("schools:teachers:courses:manage_course_list")


class CourseUpdateView(LoginRequiredMixin, OwnerCourseEditMixin, UpdateView):
    pass


class CourseDeleteView(PermissionRequiredMixin, OwnerCourseEditMixin, DeleteView):
    template_name = 'school_courses/manage/course/delete.html'
    success_url = reverse_lazy('schools:courses:manage_course_list')
    permission_required = 'school_courses.delete_schoolcourse'


class ModuleCreateUpdateView(UserPassesTestMixin, TemplateResponseMixin, View):

    def test_func(self):
        return self.request.user.account_type == "teacher"
    template_name = 'school_courses/manage/module/formset.html'
    course = None
    module = None
    form = None

    def get_course(self, request, course_slug):
        return get_object_or_404(SchoolCourse,
                                 slug=course_slug,
                                 creator=request.user.teacher_profile)

    def get_module(self, module_slug, course_id):
        return get_object_or_404(SchoolModule,
                                 id=module_slug,
                                 course=course_id)

    def dispatch(self, request, course_slug, module_slug=None):
        self.course = self.get_course(request, course_slug)

        if module_slug:
            self.module = self.get_module(module_slug, course_slug)
        return super(ModuleCreateUpdateView, self).dispatch(request, course_slug, module_slug)

    def get(self, request, *args, **kwargs):
        self.form = ModuleCreateForm(instance=self.module)

        return self.render_to_response({'module': self.module,
                                        'form': self.form})

    def post(self, request, *args, **kwargs):
        if self.module:
            self.form = ModuleCreateForm(instance=self.module, data=request.POST)
            if self.form.is_valid():
                self.form.save()
                return redirect('schools:teachers:courses:module_list')
        else:
            self.form = ModuleCreateForm(data=request.POST)
            if self.form.is_valid():
                form = self.form
                SchoolModule.objects.create(course=self.course,
                                            title=form.cleaned_data['title'],
                                            description=form.cleaned_data['description'])
                return redirect('schools:teachers:courses:manage_course_list')
        return self.render_to_response({'module': self.module,
                                        'formset': self.form})


class ContentCreateUpdateView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):

    def test_func(self):
        return self.request.user.account_type == "teacher"

    module = None
    model = None
    obj = None
    template_name = 'school_courses/manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['stext', 'svideo', 'simage', 'sfile']:
            return apps.get_model(app_label='school_courses',
                                  model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['creator',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_slug, model_name, id=None):
        self.module = get_object_or_404(SchoolModule,
                                        slug=module_slug,
                                        course__creator=request.user.teacher_profile)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         creator=request.user.teacher_profile)
        return super(ContentCreateUpdateView,
                     self).dispatch(request, module_slug, model_name, id)

    def get(self, request, module_slug, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj,
                                        'model': model_name})

    def post(self, request, module_slug, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user.teacher_profile
            obj.save()
            if not id:
                # new content
                SchoolContent.objects.create(module=self.module,
                                             item=obj)
            return redirect('schools:teachers:courses:module_content_list', self.module.id)

        return self.render_to_response({'form': form,
                                        'object': self.obj,
                                        'model': model_name})


class ContentDeleteView(UserPassesTestMixin, LoginRequiredMixin, View):

    def test_func(self):
        return self.request.user.account_type == "admin" or self.request.user.account_type == "teacher" or \
               self.request.user.account_type == "school"

    def post(self, request, id):
        content = get_object_or_404(SchoolContent,
                                    id=id,
                                    module__course__creator=request.user.teacher_profile)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('schools:teachers:courses:module_list', module.id)


class ModuleListView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'school_courses/manage/module/list.html'
    module = None
    course = None

    def test_func(self):
        return self.request.user.account_type == "teacher" or \
               self.request.user.account_type == "school"

    def get(self, request, course_slug):
        if request.user.account_type == 'teacher':
            self.module = SchoolModule.objects.filter(course=course_slug,
                                                      course__creator=request.user.teacher_profile)
            self.course = get_object_or_404(SchoolCourse,
                                            slug=course_slug)
        elif request.user.account_type == 'school':
            self.module = SchoolModule.objects.filter(course=course_slug,
                                                      course__creator__school=request.user.school_profile)
            self.course = get_object_or_404(SchoolCourse,
                                            id=course_slug)
        return self.render_to_response({'module': self.module,
                                        'course': self.course})


class ModuleContentListView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'school_courses/manage/module/content_list.html'
    module = None

    def test_func(self):
        return self.request.user.account_type == "teacher" or \
               self.request.user.account_type == "school"

    def get(self, request, module_slug):
        if request.user.account_type == 'teacher':
            self.module = get_object_or_404(SchoolModule,
                                            slug=module_slug,
                                            course__creator=request.user.teacher_profile)
        elif request.user.account_type == 'school':
            self.module = get_object_or_404(SchoolModule,
                                            slug=module_slug,
                                            course__creator__school=request.user.school_profile)
        return self.render_to_response({'module': self.module})


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):

    def post(self, request):
        for id, order in self.request_json.items():
            SchoolModule.objects.filter(id=id,
                                        course__creator=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            SchoolContent.objects.filter(id=id,
                                         module__course__creator=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class CourseListView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    model = SchoolCourse
    template_name = 'school_courses/course/list.html'
    courses = None

    def test_func(self):
        return self.request.user.account_type == "admin" or \
               self.request.user.account_type == "school"

    def get(self, request, subject=None):
        if self.request.user.account_type == 'school':
            # subjects = SchoolSubject.objects.filter(courses__creator__school=self.request.user.school_profile).annotate(
            #     total_courses=Count('courses'))
            # courses = SchoolCourse.objects.filter(school=self.request.user.school_profile).annotate(
            #     total_modules=Count('modules'))
            #
            # if subject:
            #     subject = get_object_or_404(SchoolSubject, slug=subject)
            #     courses = courses.filter(subject=subject, school=self.request.user.school_profile)
            # return self.render_to_response({'subjects': subjects,
            #                                 'subject': subject,
            #                                 'courses': courses})
            self.courses = SchoolCourse.objects.filter(school=request.user.school_profile)
        else:
            # subjects = SchoolSubject.objects.annotate(
            #     total_courses=Count('courses'))
            # courses = SchoolCourse.objects.annotate(
            #     total_modules=Count('modules'))
            #
            # if subject:
            #     subject = get_object_or_404(SchoolSubject, slug=subject)
            #     courses = courses.filter(subject=subject)
            # return self.render_to_response({'subjects': subjects,
            #                                 'subject': subject,
            #                                 'courses': courses})
            self.courses = SchoolCourse.objects.all()
        return self.render_to_response({'courses': self.courses})


class CourseDetailView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    model = SchoolCourse
    template_name = 'school_courses/course/detail.html'

    def test_func(self):
        return self.request.user.account_type == "admin" or self.request.user.account_type == "teacher" or \
               self.request.user.account_type == "school"

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(
            initial={'course': self.object})
        return context


class SubjectListView(UserPassesTestMixin, LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'school_courses/manage/subject/list.html'

    def test_func(self):
        return self.request.user.account_type == "school"

    def get_form(self, *args, **kwargs):
        Form = modelform_factory(SchoolSubject, exclude=['history', 'slug', 'school'])
        return Form(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        subjects = SchoolSubject.objects.all()
        form = self.get_form()
        return self.render_to_response({'subjects': subjects,
                                        'form': form})

    def post(self, request, *args, **kwargs):
        form = self.get_form(data=request.POST)
        if form.is_valid():
            new_subject = form.save(commit=False)
            new_subject.school = request.user.school_profile
            new_subject.save()
            return redirect("school_courses:subject_list")
        return self.render_to_response({'form': form})
