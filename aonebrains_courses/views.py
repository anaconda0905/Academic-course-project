from django.apps import apps
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.forms.models import modelform_factory
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from accounts.models import Grade
from .forms import ModuleCreateForm, SubjectForm
from .models import OpenCourse, OpenModule, OpenContent, OpenSubject


class OwnerMixin(UserPassesTestMixin, object):

    def test_func(self):
        return self.request.user.account_type == "admin" or self.request.user.account_type == "curator" or \
               self.request.user.account_type == "editor"


    def get_queryset(self):
        if self.request.user.account_type == "curator":
            qs = super(OwnerMixin, self).get_queryset().filter(creator=self.request.user.curator)
        elif self.request.user.account_type == 'editor':
            qs = super(OwnerMixin, self).get_queryset().filter(creator__admin=self.request.user.editor.admin)
        elif self.request.user.account_type == 'admin':
            qs = super(OwnerMixin, self).get_queryset()
        return qs


class OwnerEditMixin(UserPassesTestMixin, object):

    def test_func(self):
        return self.request.user.account_type == "curator"
    def form_valid(self, form):
        form.instance.creator = self.request.user.curator
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = OpenCourse
    success_url = reverse_lazy('aonebrains_courses:curator_courses')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['preview', 'subject', 'title', 'overview']
    # success_url = reverse_lazy('accounts:super_admin:curators:courses:manage_course_list')
    success_url = reverse_lazy('aonebrains_courses:curator_courses')
    template_name = 'aonebrains_courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'aonebrains_courses/manage/course/list.html'


class SubjectListView(UserPassesTestMixin, TemplateResponseMixin, View):
    template_name = 'aonebrains_courses/manage/subject/list.html'

    def test_func(self):
        return self.request.user.account_type == "admin"
    # def get_form(self, *args, **kwargs):
    #     Form = modelform_factory(OpenSubject, exclude=['history', 'slug'])
    #     return Form(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        subjects = OpenSubject.objects.all()
        form = SubjectForm()
        return self.render_to_response({'subjects': subjects,
                                        'form': form})

    def post(self, request, *args, **kwargs):
        form = SubjectForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("aonebrains_courses:subject_list")
        return self.render_to_response({'form': form})


class SubjectEditView(UserPassesTestMixin, UpdateView):

    def test_func(self):
        return self.request.user.account_type == "admin"

    model = OpenSubject
    form_class = SubjectForm
    success_url = reverse_lazy('aonebrains_courses:subject_list')
    slug_field = 'slug'
    template_name = 'aonebrains_courses/manage/subject/form.html'
    # subject = None
    #
    # def get(self, request, subject_slug):
    #     self.subject = get_object_or_404(Subject,
    #                                      slug=subject_slug)
    #     form = SubjectForm(instance=self.subject)
    #     return self.render_to_response({'form': form,
    #                                     'subject': self.subject.title})
    #
    # def post(self, request):
    #     form = SubjectForm(instance=self.subject, data=request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return reverse_lazy('aonebrains_courses:subject_list')
    #     return self.render_to_response({'form':form})


class ClassListView(UserPassesTestMixin, TemplateResponseMixin, View):
    template_name = 'aonebrains_courses/manage/classes/list.html'

    def test_func(self):
        return self.request.user.account_type == "admin"
    def get_form(self, *args, **kwargs):
        Form = modelform_factory(Grade, exclude=['history', 'slug'])
        return Form(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        classes = Grade.objects.all()
        form = self.get_form()
        return self.render_to_response({'classes': classes,
                                        'form': form})

    def post(self, request, *args, **kwargs):
        form = self.get_form(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("aonebrains_courses:class_list")
        return self.render_to_response({'form': form})


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    fields = ['preview', 'subject', 'title', 'overview', 'grade']

    def form_valid(self, form):
        OpenCourse.objects.get_or_create(title=form.cleaned_data['title'],
                                         subject=form.cleaned_data['subject'],
                                         overview=form.cleaned_data['overview'],
                                         creator=self.request.user.curator,
                                         admin=self.request.user.curator.admin,
                                         grade=form.cleaned_data['grade'])
        return reverse_lazy("aonebrains_courses:curator_courses")


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    slug_field = "slug"


class CourseDeleteView(OwnerCourseEditMixin, DeleteView):
    template_name = 'delete.html'
    success_url = reverse_lazy('dashboard')
    slug_field = "slug"


class ModuleCreateUpdateView(UserPassesTestMixin, TemplateResponseMixin, View):
    template_name = 'aonebrains_courses/manage/module/formset.html'
    course = None
    module = None
    form = None

    def test_func(self):
        return self.request.user.account_type == "curator"

    def get_course(self, request, slug):
        return get_object_or_404(OpenCourse,
                                 slug=slug,
                                 creator=request.user.curator)

    def get_module(self, module_slug, course_slug):
        return get_object_or_404(OpenModule,
                                 slug=module_slug,
                                 course__slug=course_slug)

    def dispatch(self, request, course_slug, module_slug=None):
        self.course = self.get_course(request, course_slug)

        if module_slug:
            self.module = self.get_module(module_slug, course_slug)
        return super(ModuleCreateUpdateView, self).dispatch(request, course_slug, module_slug=None)

    def get(self, request, *args, **kwargs):
        if self.module:
            self.form = ModuleCreateForm(instance=self.module)
        else:
            self.form = ModuleCreateForm()
        return self.render_to_response({'module': self.module,
                                        'form': self.form})

    def post(self, request, *args, **kwargs):
        if self.module:
            self.form = ModuleCreateForm(instance=self.module, data=request.POST)
            if self.form.is_valid():
                self.form.save()
                return reverse_lazy('aonebrains_courses:curator_course_module_list', self.course.slug)
        else:
            self.form = ModuleCreateForm(data=request.POST)
            if self.form.is_valid():
                form = self.form
                OpenModule.objects.create(course=self.course,
                                          title=form.cleaned_data['title'],
                                          description=form.cleaned_data['description'])
            return redirect('aonebrains_courses:curator_course_module_list', self.course.slug)
        return self.render_to_response({'module': self.module,
                                        'formset': self.form})


class ContentCreateUpdateView(UserPassesTestMixin, TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'aonebrains_courses/manage/content/form.html'

    def test_func(self):
        return self.request.user.account_type == "curator"

    def get_model(self, model_name):
        if model_name in ['atext', 'avideo', 'aimage', 'afile']:
            return apps.get_model(app_label='aonebrains_courses',
                                  model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['creator',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_slug, model_name, id=None):
        self.module = get_object_or_404(OpenModule,
                                        slug=module_slug)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id)
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
            obj.creator = request.user.curator
            obj.save()
            if not id:
                # new content
                OpenContent.objects.create(module=self.module,
                                           item=obj)
            return reverse_lazy('aonebrains_courses:module_content_list', module_slug)

        return self.render_to_response({'form': form,
                                        'object': self.obj})


class ContentDeleteView(UserPassesTestMixin, TemplateResponseMixin, View):
    template_name = 'delete.html'
    content = None

    def test_func(self):
        return self.request.user.account_type == "admin" or self.request.user.account_type == "super admin" or \
               self.request.user.account_type == "curator"

    def post(self, request, id):
        if request.user.account_type == 'curator':
            self.content = get_object_or_404(OpenContent,
                                    id=id,
                                    module__course__creator=request.user.curator)
        elif request.user.account_type == "super admin":
            self.content = get_object_or_404(OpenContent,
                                             id=id,
                                             module__course__creator__admin=request.user.super_admin_profile)
        elif request.user.account_type == "admin":
            self.content = get_object_or_404(OpenContent,
                                             id=id, )
        else:
            raise PermissionDenied

        module = self.content.module
        self.content.item.delete()
        self.content.delete()
        return reverse_lazy('aonebrains_courses:module_content_list', module.slug)


class ModuleListView(UserPassesTestMixin, TemplateResponseMixin, View):
    template_name = 'aonebrains_courses/manage/module/list.html'
    module = None
    course = None

    def test_func(self):
        return self.request.user.account_type == "admin" or self.request.user.account_type == "super admin" or \
               self.request.user.account_type == "curator"

    def get(self, request, course_slug):
        if request.user.account_type == 'curator':
            self.module = OpenModule.objects.filter(course__slug=course_slug,
                                                    course__creator=request.user.curator)
            self.course = get_object_or_404(OpenCourse,
                                            slug=course_slug)
        elif request.user.account_type == 'super admin':
            self.module = OpenModule.objects.filter(course__slug=course_slug,
                                                    course__creator__admin=request.user.super_admin_profile)
            self.course = get_object_or_404(OpenCourse,
                                            slug=course_slug)
        elif request.user.account_type == 'admin':
            self.module = OpenModule.objects.filter(course__slug=course_slug)
            self.course = get_object_or_404(OpenCourse,
                                            slug=course_slug)

        return self.render_to_response({'module': self.module,
                                        'course': self.course})


class ModuleContentListView(UserPassesTestMixin, TemplateResponseMixin, View):
    template_name = 'aonebrains_courses/manage/module/content_list.html'
    module = None

    def test_func(self):
        return self.request.user.account_type == "admin" or self.request.user.account_type == "super admin" or \
               self.request.user.account_type == "curator"

    def get(self, request, module_slug):
        if request.user.account_type == 'curator':
            self.module = get_object_or_404(OpenModule,
                                            slug=module_slug,
                                            course__creator=request.user.curator)
        elif request.user.account_type == 'super admin':
            self.module = get_object_or_404(OpenModule,
                                            slug=module_slug,
                                            course__creator__admin=request.user.super_admin_profile)
        elif request.user.account_type == 'admin':
            self.module = get_object_or_404(OpenModule,
                                            slug=module_slug)
        return self.render_to_response({'module': self.module})


# class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
#
#     def post(self, request):
#         for id, order in self.request_json.items():
#             OpenModule.objects.filter(id=id).update(order=order)
#         return self.render_json_response({'saved': 'OK'})
#
#
# class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
#     def post(self, request):
#         for id, order in self.request_json.items():
#             OpenContent.objects.filter(id=id).update(order=order)
#         return self.render_json_response({'saved': 'OK'})


class CourseListView(UserPassesTestMixin, TemplateResponseMixin, View):
    template_name = 'aonebrains_courses/course/list.html'
    subjects = None
    subject = None
    courses = None

    def test_func(self):
        return self.request.user.account_type == "admin" or self.request.user.account_type == "super admin" or \
               self.request.user.account_type == "editor"

    def get(self, request, subject=None):
        if request.user.account_type == 'super admin':
            self.courses = OpenCourse.objects.filter(admin=request.user.super_admin_profile)

        elif request.user.account_type == 'editor':
            self.courses = OpenCourse.objects.filter(admin=request.user.editor.admin)

        elif request.user.account_type == 'admin':
            self.courses = OpenCourse.objects.all()

        return self.render_to_response({'subjects': self.subjects,
                                        'subject': self.subject,
                                        'courses': self.courses})


class ModuleDeleteView(UserPassesTestMixin, DeleteView):

    def test_func(self):
        return self.request.user.account_type == "admin" or self.request.user.account_type == "super admin" or \
               self.request.user.account_type == "curator"

    model = OpenModule
    template_name = 'delete.html'
    success_url = reverse_lazy('aonebrains_courses:course_list')
    slug_field = 'slug'


# class CourseDetailView(DetailView):
#     model = OpenCourse
#     template_name = 'aonebrains_courses/course/detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(CourseDetailView, self).get_context_data(**kwargs)
#         context['enroll_form'] = CourseEnrollForm(
#             initial={'course': self.object})
#         return context


class CuratorCoursesListView(UserPassesTestMixin, ListView):
    model = OpenCourse
    template_name = 'aonebrains_courses/course/list.html'
    context_object_name = 'courses'

    def test_func(self):
        return self.request.user.account_type == "admin" or self.request.user.account_type == "super admin" or \
               self.request.user.account_type == "editor"

    def get_queryset(self):
        qs = super(CuratorCoursesListView, self).get_queryset()
        return qs.filter(creator__slug=self.kwargs['curator_slug'])


# class CuratorCourseDetailView(DetailView, OwnerMixin):
#     template_name = "aonebrains_courses/course/detail.html"
#     slug_field = "slug"
#     model = OpenCourse

class CuratorCourseDetailView(UpdateView, OwnerMixin):


    model = OpenCourse
    fields = ['preview', 'title', 'overview', 'subject', 'grade', 'draft', 'approved']
    template_name = "aonebrains_courses/course/detail.html"
    slug_field = "slug"
    success_url = reverse_lazy("aonebrains_courses:course_list")


class CuratorCourseModuleDetailView(DetailView, OwnerMixin):

    model = OpenModule
    template_name = "aonebrains_courses/course/module/detail.html"
    slug_field = 'slug'
    success_url = reverse_lazy("aonebrains_courses:course_list")


class GradeCoursesListView(UserPassesTestMixin, ListView):
    model = OpenCourse
    context_object_name = 'courses'
    template_name = 'aonebrains_courses/course/list.html'

    def test_func(self):
        return self.request.user.account_type == "admin"

    def get_queryset(self):
        qs = super(GradeCoursesListView, self).get_queryset()
        return qs.filter(grade__slug=self.kwargs['grade_slug'])


class SubjectCourseListView(UserPassesTestMixin, ListView):
    model = OpenCourse
    context_object_name = 'courses'
    template_name = 'aonebrains_courses/course/list.html'

    def test_func(self):
        return self.request.user.account_type == "admin"

    def get_queryset(self):
        qs = super(SubjectCourseListView, self).get_queryset()
        return qs.filter(subject__slug=self.kwargs['subject_slug'])


class GradeDeleteView(UserPassesTestMixin, DeleteView):

    def test_func(self):
        return self.request.user.account_type == "admin"

    model = Grade
    slug_field = "slug"
    template_name = 'delete.html'
    success_url = reverse_lazy('aonebrains_courses:class_list')


class SubjectDeleteView(UserPassesTestMixin, DeleteView):

    def test_func(self):
        return self.request.user.account_type == "admin"

    model = OpenSubject
    slug_field = "slug"
    template_name = 'delete.html'
    success_url = reverse_lazy('aonebrains_courses:subject_list')


class ContentDetailView(UserPassesTestMixin, DetailView):

    def test_func(self):
        return self.request.user.account_type == "admin" or self.request.user.account_type == "super admin"

    model = OpenContent
    template_name = 'aonebrains_courses/content/detail.html'
