from django import forms
from django.forms.models import inlineformset_factory

from .models import SchoolCourse, SchoolModule


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=SchoolCourse.objects.all(),
                                    widget=forms.HiddenInput)


ModuleFormSet = inlineformset_factory(SchoolCourse,
                                      SchoolModule,
                                      fields=['title',
                                              'description'],
                                      extra=0,
                                      can_delete=True)


class ModuleCreateForm(forms.ModelForm):
    class Meta:
        model = SchoolModule
        fields = ['title', 'description']
