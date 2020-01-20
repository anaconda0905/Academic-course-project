from django import forms
from django.forms.models import inlineformset_factory

from .models import OpenCourse, OpenModule, OpenSubject


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=OpenCourse.objects.all(),
                                    widget=forms.HiddenInput)


ModuleFormSet = inlineformset_factory(OpenCourse,
                                      OpenModule,
                                      fields=['title',
                                              'description'],
                                      extra=0,
                                      can_delete=True)


class ModuleCreateForm(forms.ModelForm):
    class Meta:
        model = OpenModule
        fields = ['title', 'description', 'order']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = OpenSubject
        fields = ['title']
