from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.db import transaction

from accounts.groups import CuratorGroup
from accounts.task import user_send_mail
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = User
        fields = ['username', 'email', 'is_staff', 'is_active', 'account_type', 'country', 'city', 'phone', 'mobile']


class CuratorSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    @transaction.atomic()
    def save(self, commit=True):
        user = super(CuratorSignUpForm, self).save(commit=False)
        user.account_type = 'curator'
        # Group.objects.get_or_create(name="Curator")
        # user_group = Group.objects.get(name="Curator")
        password = User.objects.make_random_password()
        user.set_password(password)
        # print(password)
        user.save()
        CuratorGroup(user)
        # file = open('curator.txt', 'a')
        # file.write("{:<20}{:>10}\n".format(user.username, password))
        # file.close()
        user_send_mail.delay(user=user, password=password)
        # send_mail('Account Password', 'UserName: {}\n'
        #                               'First Name: {}\n'
        #                               'Last Name: {}\n'
        #                               'Password for your account is {}'
        #                               ''.format(user.username, user.first_name, user.last_name, password),
        #           settings.EMAIL_HOST_USER,
        #           [user.email])
        # user_group.user_set.add(user)
        return user


class SuperAdminSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone']

    @transaction.atomic()
    def save(self, request, commit=True):
        user = super(SuperAdminSignUpForm, self).save(commit=False)
        user.account_type = 'super admin'
        Group.objects.get_or_create(name="Super Admin")
        user_group = Group.objects.get(name="Super Admin")
        password = User.objects.make_random_password()
        user.set_password(password)
        # print(password)
        # file = open('Super_Admin.txt', 'a')
        # file.write("{:<20}{:>10}\n".format(user.username, password))
        # file.close()
        user_send_mail.delay(user=user, password=password)
        # send_mail('Account Password', 'UserName: {}\n'
        #                               'First Name: {}\n'
        #                               'Last Name: {}\n'
        #                               'Password for your account is {}'
        #                               ''.format(user.username, user.first_name, user.last_name, password),
        #           settings.EMAIL_HOST_USER,
        #           [user.email])
        user.save()
        user_group.user_set.add(user)
        return user


class EditorSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    @transaction.atomic()
    def save(self, commit=True):
        user = super(EditorSignUpForm, self).save(commit=False)
        user.account_type = 'editor'
        Group.objects.get_or_create(name="Editor")
        user_group = Group.objects.get(name="Editor")
        password = User.objects.make_random_password()
        user.set_password(password)
        # print(password)
        # file = open('editor.txt', 'a')
        # file.write("{:<20}{:>10}".format(user.username, password))
        # file.close()
        user_send_mail.delay(user=user, password=password)
        # send_mail('Account Password', 'UserName: {}\n'
        #                               'First Name: {}\n'
        #                               'Last Name: {}\n'
        #                               'Password for your account is {}'
        #                               ''.format(user.username, user.first_name, user.last_name, password),
        #           settings.EMAIL_HOST_USER,
        #           [user.email])
        user.save()
        user_group.user_set.add(user)
        return user


class MarketerSignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    @transaction.atomic()
    def save(self, commit=True):
        user = super(MarketerSignUpForm, self).save(commit=False)
        user.account_type = 'marketer'
        Group.objects.get_or_create(name="Marketer")
        user_group = Group.objects.get(name="Marketer")
        password = User.objects.make_random_password()
        user.set_password(password)
        # print(password)
        # file = open('Marketer.txt', 'a')
        # file.write("{:<20}{:>10}".format(user.username, password))
        # file.close()
        user_send_mail.delay(user=user, password=password)
        # send_mail('Account Password', 'UserName: {}\n'
        #                               'First Name: {}\n'
        #                               'Last Name: {}\n'
        #                               'Password for your account is {}'
        #                               ''.format(user.username, user.first_name, user.last_name, password),
        #           settings.EMAIL_HOST_USER,
        #           [user.email])
        user.save()
        user_group.user_set.add(user)
        return user


class UserProfileForm(forms.ModelForm):
    # Same form used by Super Admins, Curators, Editors, Teachers and Students
    class Meta:
        model = User
        fields = ['avatar', 'username', 'first_name', 'last_name', 'email', 'address', 'country', 'city', 'phone',
                  'mobile', 'is_active']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = True

    # def __init__(self, *args, **kwargs):
    #     super(UserProfileForm, self).__init__(*args, **kwargs)
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.id:
    #         self.fields['username'].widget.attrs['readonly'] = True
    #
    # def clean_foo_field(self):
    #     instance = getattr(self, 'instance', None)
    #     if instance and instance.id:
    #         return instance.name
    #     else:
    #         return self.cleaned_data['username']


class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', "password1", "password2"]

    @transaction.atomic()
    def save(self, commit=True):
        user = super(StudentSignUpForm, self).save(commit=False)
        user.account_type = 'aonestudent'
        Group.objects.get_or_create(name="Aone Student")
        user_group = Group.objects.get(name="Aone Student")
        user.save()
        user_group.user_set.add(user)
        return user
