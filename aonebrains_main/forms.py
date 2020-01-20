from django import forms

from aonebrains_courses.models import OpenCourse
from school_courses.models import SchoolCourse


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=OpenCourse.objects.all(),
                                    widget=forms.HiddenInput)


class SchoolCourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=SchoolCourse.objects.all(),
                                    widget=forms.HiddenInput)
