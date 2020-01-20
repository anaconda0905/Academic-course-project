from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.db import transaction

from accounts.models import User
from accounts.task import user_send_mail
from schools.models import School
from .models import Teacher


# Create your models here.


class SchoolSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self, commit=True):
        user = super(SchoolSignUpForm, self).save(commit=False)
        user.account_type = 'school'
        Group.objects.get_or_create(name="Schools")
        user_group = Group.objects.get(name="Schools")
        user.save()
        user_group.user_set.add(user)
        return user


class MarketerSchoolSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    @transaction.atomic
    def save(self, commit=True):
        user = super(MarketerSchoolSignUpForm, self).save(commit=False)
        user.account_type = 'school'
        Group.objects.get_or_create(name="Schools")
        user_group = Group.objects.get(name="Schools")
        password = User.objects.make_random_password()
        user.set_password(password)
        # print(password)
        # file = open('school.txt', 'a')
        # file.write("{:<20}{:>10}\n".format(user.username, password))
        # file.close()
        user_send_mail.delay(user=user, password=password)
        # send_mail('Account Password', 'UserName: {}\n'
        #                               'Password for your account is {}'
        #                               ''.format(user.username, password),
        #           settings.EMAIL_HOST_USER,
        #           [user.email])
        user.save()
        user_group.user_set.add(user)
        return user


class SchoolUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'address', 'country', 'city', 'phone', 'mobile']

    def __init__(self, *args, **kwargs):
        super(SchoolUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = True

    # def __init__(self, *args, **kwargs):
    #     super(SchoolUserForm, self).__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.id:
    #         self.fields['username'].widget.attrs['readonly'] = True
    #
    # def clean_foo_field(self):
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.id:
    #         return instance.username
    #     else:
    #         return self.cleaned_data['username']


class SchoolProfileForm(forms.ModelForm):
    class Meta:
        model = School
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(SchoolProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].disabled = True

    # def __init__(self, *args, **kwargs):
    #     super(SchoolProfileForm, self).__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.pk:
    #         if self.instance.name == '':
    #             print(self.instance.name)
    #             print("AAAAAAAAAA")
    #             self.fields['name'].widget.attrs['readonly'] = False
    #         else:
    #             print("BBBBBBBBBBB")
    #             self.fields['name'].widget.attrs['readonly'] = True
    #
    # def clean_name_field(self):
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.pk:
    #         return self.instance.name
    #     else:
    #         return self.cleaned_data['name']


class TeacherSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    @transaction.atomic()
    def save(self, request, commit=True):
        user = super(TeacherSignUpForm, self).save(commit=False)
        user.account_type = 'teacher'
        Group.objects.get_or_create(name="Teachers")
        user_group = Group.objects.get(name="Teachers")
        password = User.objects.make_random_password()
        user.set_password(password)
        # print(password)
        # file = open('teacher.txt', 'a')
        # file.write("{:<20}{:>10}\n".format(user.username, password))
        # file.close()
        user_send_mail.delay(user=user, password=password, host=request.user.email)
        # send_mail('Account Password', 'UserName: {}\n'
        #                               'First Name: {}\n'
        #                               'Last Name: {}\n'
        #                               'Password for your account is {}'
        #                               ''.format(user.username, user.first_name, user.last_name, password),
        #           request.user.email,
        #           [user.email])
        user.save()
        user_group.user_set.add(user)
        return user


class StudentSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone']

    @transaction.atomic
    def save(self, request, commit=True):
        user = super(StudentSignUpForm, self).save(commit=False)
        user.account_type = 'student'
        Group.objects.get_or_create(name="Students")
        user_group = Group.objects.get(name='Students')
        password = User.objects.make_random_password()
        user.set_password(password)
        # print(password)
        # file = open('student.txt', 'a')
        # file.write("{:<20}{:>10}\n".format(user.username, password))
        # file.close()
        user_send_mail.delay(user=user, password=password, host=request.user.email)
        # send_mail('Account Password', 'UserName: {}\n'
        #                               'First Name: {}\n'
        #                               'Last Name: {}\n'
        #                               'Password for your account is {}'
        #                               ''.format(user.username, user.first_name, user.last_name, password),
        #           request.user.email,
        #           [user.email])
        user.save()
        user_group.user_set.add(user)
        return user


class TeacherClassForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['grade']


class TeacherStudentForm(forms.Form):
    username = forms.CharField(max_length=150, help_text='Enter SchoolStudent username')
