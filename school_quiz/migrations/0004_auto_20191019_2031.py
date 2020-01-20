# Generated by Django 2.2.3 on 2019-10-20 03:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('school_quiz', '0003_auto_20191019_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE,
                                    to='school_quiz.MCQQuestion', verbose_name='Question'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mcqquestion',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='school_courses.SchoolCourse', verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='mcqquestion',
            name='quiz',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='questions', to='school_quiz.Quiz', verbose_name='Quiz'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='school_courses.SchoolCourse', verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='sitting',
            name='quiz',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='school_quiz.Quiz',
                                    verbose_name='Quiz'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sitting',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='schools.SchoolStudent',
                                    verbose_name='Student'),
            preserve_default=False,
        ),
    ]
