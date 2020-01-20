from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_reverse_admin import ReverseModelAdmin
from reversion.admin import VersionAdmin
from simple_history.admin import SimpleHistoryAdmin

from aonebrains_quiz.models import Quiz, MCQQuestion, Answer, Progress, Sitting
from schools.models import (
    Grade
)
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, SuperAdmin, Curator, Editor, Student, Marketer

admin.site.site_header = 'AoneBrains'


# class AuthForm(forms.ModelForm):
#     error_messages = {
#         'password_mismatch': _("The two password fields didn't match."),
#     }
#     password1 = forms.CharField(
#         label=_("Password"),
#         strip=False,
#         widget=forms.PasswordInput,
#         help_text=password_validation.password_validators_help_text_html(),
#     )
#     password2 = forms.CharField(
#         label=_("Password confirmation"),
#         widget=forms.PasswordInput,
#         strip=False,
#         help_text=_("Enter the same password as before, for verification."),
#     )
#
#     class Meta:
#         model = User
#         fields = ['password1', 'password2']
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError(
#                 self.error_messages['password_mismatch'],
#                 code='password_mismatch',
#             )
#         return password2
#
#     def _post_clean(self):
#         super()._post_clean()
#         # Validate the password after self.instance is updated with form data
#         # by super().
#         password = self.cleaned_data.get('password2')
#         if password:
#             try:
#                 password_validation.validate_password(password, self.instance)
#             except forms.ValidationError as error:
#                 self.add_error('password2', error)
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user


class PersonAdmin(ReverseModelAdmin):
    inline_type = 'stacked'
    inline_reverse = [
        ('user', {'fields': ['first_name', 'last_name', 'username', 'email']}),
    ]
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'password1', 'password2')}
         ),
    )


class CustomUserAdmin(UserAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['name', 'user__username']

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'username', ]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Extra Info', {'fields': ('avatar', 'address', 'country', 'city', 'phone', 'mobile', 'account_type')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
         ),
    )


class AnswerInline(admin.StackedInline):
    model = Answer


# class QuizAdminForm(forms.ModelForm):
#     """
#         below is from
#         http://stackoverflow.com/questions/11657682/
#         django-admin-interface-using-horizontal-filter-with-
#         inline-manytomany-field
#     """
#
#     class Meta:
#         model = Quiz
#         exclude = []
#
#     questions = forms.ModelMultipleChoiceField(
#         queryset=MCQQuestion.objects.all().select_subclasses(),
#         required=False,
#         label=_("Questions"),
#         widget=FilteredSelectMultiple(
#             verbose_name=_("Questions"),
#             is_stacked=False))
#
#     def __init__(self, *args, **kwargs):
#         super(QuizAdminForm, self).__init__(*args, **kwargs)
#         if self.instance.pk:
#             self.fields['questions'].initial = \
#                 self.instance.questions.all().select_subclasses()
#
#     def save(self, commit=True):
#         quiz = super(QuizAdminForm, self).save(commit=False)
#         quiz.save()
#         quiz.questions.set(self.cleaned_data['questions'])
#         self.save_m2m()
#         return quiz


# class QuizAdmin(admin.ModelAdmin):
#     form = QuizAdminForm
#
#     list_display = ('title',)
#
#     search_fields = ('description', 'course',)


class MCQuestionAdmin(admin.ModelAdmin):
    list_display = ('content',)
    fields = ('content', 'course',
              'figure', 'quiz', 'explanation', 'answer_order')

    search_fields = ('content', 'explanation')
    # filter_horizontal = ('quiz',)

    inlines = [AnswerInline]


class ProgressAdmin(admin.ModelAdmin):
    """
    to do:
            create a user section
    """
    search_fields = ('student', 'score',)


# Register your models here.
# admin.site.register(User, CustomUserAdmin)
# admin.site.register(School)
# admin.site.register(SchoolStudent)
# admin.site.register(Teacher)
# admin.site.register(SchoolCourse)
# admin.site.register(SchoolContent)
# admin.site.register(SchoolSubject)
# admin.site.register(SchoolModule)
# admin.site.register(Grade, SimpleHistoryAdmin)
# admin.site.register(SuperAdmin, SimpleHistoryAdmin)
# admin.site.register(Curator, SimpleHistoryAdmin)
# admin.site.register(Editor, VersionAdmin)
# admin.site.register(OpenCourse)
# admin.site.register(OpenSubject)
# admin.site.register(OpenContent)
# admin.site.register(OpenModule)
admin.site.register(Progress)
admin.site.register(Sitting)


# admin.site.register(Quiz, QuizAdmin)
# admin.site.register(MCQQuestion, MCQuestionAdmin)

@admin.register(User)
class UserAdmin(VersionAdmin, SimpleHistoryAdmin, CustomUserAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(Editor)
class EditorAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(Curator)
class CuratorAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(SuperAdmin)
class SuperAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(Quiz)
class QuizAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(MCQQuestion)
class MCQAdmin(VersionAdmin, SimpleHistoryAdmin, MCQuestionAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(Grade)
class GradeAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(Student)
class StudentAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']


@admin.register(Marketer)
class StudentAdmin(VersionAdmin, SimpleHistoryAdmin):
    # list_display = ["id", "name", "status"]
    history_list_display = ["status"]
    search_fields = ['user__username']
