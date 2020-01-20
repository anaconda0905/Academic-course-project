from django import forms
from django.forms.models import inlineformset_factory
from django.forms.widgets import RadioSelect

from .models import MCQQuestion, Answer, Quiz


class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answers_list()]
        self.fields["answers"] = forms.ChoiceField(choices=choice_list, widget=RadioSelect)


MCQFormSet = inlineformset_factory(MCQQuestion,
                                   Answer,
                                   fields=['content',
                                           'correct'],
                                   extra=4,
                                   can_delete=True,
                                   )


class QuizCreateForm(forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = ['course', 'slug']


class MCQCreateForm(forms.ModelForm):
    class Meta:
        model = MCQQuestion
        exclude = ['course', 'quiz']

# class AnswerForm(forms.ModelForm):
#     class Meta:
#         model = Answer
#         exclude = ['question']
#
