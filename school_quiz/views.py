from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, TemplateView, ListView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import FormView

from school_courses.models import SchoolCourse
from .forms import QuestionForm, MCQFormSet
from .forms import QuizCreateForm, MCQCreateForm
from .models import Quiz, Progress, Sitting, MCQQuestion


# Create your views here.


class QuizCreateUpdateView(TemplateResponseMixin, View):
    template_name = "school_quiz/quiz/manage/quiz/form.html"
    course = None
    quiz = None

    def get_course(self, request, pk):
        return get_object_or_404(SchoolCourse,
                                 id=pk,
                                 creator=request.user.teacher_profile)

    def get_quiz(self, course_id, quiz_id):
        return get_object_or_404(Quiz,
                                 id=quiz_id,
                                 course=course_id)

    #
    # def get_form(self, *args, **kwargs):
    #     Form = modelform_factory(Quiz, exclude=['course',
    #                                             'slug'])
    #     return Form(*args, **kwargs)

    def dispatch(self, request, course_id, quiz_id=None):
        self.course = self.get_course(request, course_id)

        if quiz_id:
            self.quiz = self.get_quiz(course_id, quiz_id)
        return super(QuizCreateUpdateView, self).dispatch(request, course_id, quiz_id)

    def get(self, request, course_id, quiz_id):
        form = QuizCreateForm(instance=self.quiz)
        return self.render_to_response({'quiz': self.quiz,
                                        'form': form,
                                        'course': self.course})

    def post(self, request, course_id, quiz_id):
        form = QuizCreateForm(instance=self.quiz, data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.course = self.course
            form.creator = request.user.teacher_profile
            form.save()
            return redirect("schools:teachers:courses:quiz_list", course_id)

        return self.render_to_response({'quiz': self.quiz,
                                        'form': form,
                                        'course': self.course})


class MCQCreateUpdateView(TemplateResponseMixin, View):
    template_name = 'school_quiz/quiz/manage/mcq/form.html'
    course = None
    quiz = None
    mcq = None
    form = None
    ans_form = None

    def get_course(self, request, pk):
        return get_object_or_404(SchoolCourse,
                                 id=pk,
                                 creator=request.user.teacher_profile)

    def get_quiz(self, course_id, quiz_id):
        return get_object_or_404(Quiz,
                                 id=quiz_id,
                                 course=course_id)

    def get_MCQ(self, quiz_id, mcq_id):
        return get_object_or_404(MCQQuestion,
                                 id=mcq_id,
                                 quiz=quiz_id)

    def dispatch(self, request, course_id, quiz_id, mcq_id=None):
        self.course = self.get_course(request, course_id)
        self.quiz = self.get_quiz(course_id, quiz_id)

        if mcq_id:
            self.mcq = self.get_MCQ(quiz_id, mcq_id)
        return super(MCQCreateUpdateView, self).dispatch(request, course_id, quiz_id)

    def get(self, request, course_id, quiz_id):
        mcq_form = MCQCreateForm(instance=self.mcq)
        ans_form = MCQFormSet(instance=self.mcq)
        return self.render_to_response({'mcq': self.mcq,
                                        'mcq_form': mcq_form,
                                        'ans_form': ans_form,
                                        })

    def post(self, request, course_id, quiz_id):
        self.form = MCQCreateForm(instance=self.mcq, data=request.POST)
        if self.form.is_valid():
            mcq_form = self.form.save(commit=False)
            # ans_form = self.ans_form.save(commit=False)
            mcq_form.course = self.course
            mcq_form.quiz = self.quiz
            mcq_form.save()
            self.ans_form = MCQFormSet(instance=mcq_form, data=request.POST)
            if self.ans_form.is_valid():
                self.ans_form.save()
                return redirect("schools:teachers:courses:mcq_list", quiz_id)
        return self.render_to_response({'mcq': self.mcq,
                                        'mcq_form': self.form,
                                        'ans_form': self.ans_form,
                                        })


class QuizListView(TemplateResponseMixin, View):
    template_name = "school_quiz/quiz/manage/quiz/list.html"
    quizzes = None

    # @login_required

    def get(self, request, course_id, *args, **kwargs):
        self.quizzes = Quiz.objects.filter(course=course_id)
        return self.render_to_response({'quizzes': self.quizzes,
                                        'course_id': course_id})


class MCQListView(TemplateResponseMixin, View):
    template_name = "school_quiz/quiz/manage/mcq/list.html"
    mcq = None

    # @login_required

    def get(self, request, course_id, quiz_id, *args, **kwargs):
        self.mcq = MCQQuestion.objects.filter(course=course_id, quiz=quiz_id)
        return self.render_to_response({'mcqs': self.mcq,
                                        'quiz_id': quiz_id,
                                        'course_id': course_id})


class QuizDetailView(DetailView):
    model = Quiz
    slug_field = 'slug'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ViewQuizListByCourses(ListView):
    model = Quiz
    course = None

    # template_name = 'view_quiz_category.html'

    def dispatch(self, request, course_id, *args, **kwargs):
        self.course = get_object_or_404(
            SchoolCourse,
            course=course_id
        )

        return super(ViewQuizListByCourses, self). \
            dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ViewQuizListByCourses, self) \
            .get_context_data(**kwargs)

        context['course'] = self.course
        return context

    def get_queryset(self):
        queryset = super(ViewQuizListByCourses, self).get_queryset()
        return queryset.filter(course=self.course, draft=False)


class QuizStudentProgressView(TemplateView):
    template_name = 'school_quiz/quiz/manage/quiz/take/progress.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(QuizStudentProgressView, self) \
            .dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuizStudentProgressView, self).get_context_data(**kwargs)
        progress, c = Progress.objects.get_or_create(student=self.request.user.school_student_profile)
        context['cat_scores'] = progress.list_all_cou_scores(enrolled_student=self.request.user.school_student_profile)
        context['exams'] = progress.show_exams()
        return context


class QuizTake(FormView):
    form_class = QuestionForm
    quiz = None
    template_name = 'aonebrains_quiz/quiz/manage/quiz/take/question.html'
    correct_ans = 0
    wrong_ans = 0

    def dispatch(self, request, quiz_slug, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, slug=quiz_slug)
        if self.quiz.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        self.logged_in_user = self.request.user.is_authenticated

        if self.logged_in_user:
            self.sitting = Sitting.objects.user_sitting(request.user.school_student_profile,
                                                        self.quiz)
        if self.sitting is False:
            return render(request, 'school_quiz/quiz/manage/quiz/take/single_complete.html')

        return super(QuizTake, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class=QuestionForm):
        if self.logged_in_user:
            self.question = self.sitting.get_first_question()
            self.progress = self.sitting.progress()
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizTake, self).get_form_kwargs()

        return dict(kwargs, question=self.question)

    def form_valid(self, form):
        if self.logged_in_user:
            self.form_valid_user(form)
            if self.sitting.get_first_question() is False:
                return self.final_result_user()
        self.request.POST = {}

        return super(QuizTake, self).get(self, self.request)

    def get_context_data(self, **kwargs):
        context = super(QuizTake, self).get_context_data(**kwargs)
        context['question'] = self.question
        context['quiz'] = self.quiz
        if hasattr(self, 'previous'):
            context['previous'] = self.previous
        if hasattr(self, 'progress'):
            context['progress'] = self.progress
        return context

    def form_valid_user(self, form):
        progress, c = Progress.objects.get_or_create(student=self.request.user.school_student_profile)
        guess = form.cleaned_data['answers']
        is_correct = self.question.check_if_correct(guess)

        if is_correct is True:
            self.sitting.add_to_score(1)
            progress.update_score(self.question, 1, 1)
            self.correct_ans += 1
            progress.correct_answer = self.correct_ans
        else:
            self.sitting.add_incorrect_question(self.question)
            progress.update_score(self.question, 0, 1)
            self.wrong_ans += 1
            progress.wrong_answer = self.wrong_ans

        if self.quiz.answers_at_end is not True:
            self.previous = {'previous_answer': guess,
                             'previous_outcome': is_correct,
                             'previous_question': self.question,
                             'answers': self.question.get_answers(),
                             'question_type': {self.question
                                                   .__class__.__name__: True}}
        else:
            self.previous = {}

        self.sitting.add_user_answer(self.question, guess)
        self.sitting.remove_first_question()

    def final_result_user(self):
        results = {
            'quiz': self.quiz,
            'score': self.sitting.get_current_score,
            'max_score': self.sitting.get_max_score,
            'percent': self.sitting.get_percent_correct,
            'sitting': self.sitting,
            'previous': self.previous,
        }

        self.sitting.mark_quiz_complete()

        if self.quiz.answers_at_end:
            results['questions'] = \
                self.sitting.get_questions(with_answers=True)
            results['incorrect_questions'] = \
                self.sitting.get_incorrect_questions

        return render(self.request, 'school_quiz/quiz/manage/quiz/take/result.html', results)
