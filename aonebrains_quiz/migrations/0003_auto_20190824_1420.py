# Generated by Django 2.2.3 on 2019-08-24 21:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('aonebrains_quiz', '0002_auto_20190824_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mcqquestion',
            name='quiz',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='aonebrains_quiz.Quiz', verbose_name='Quiz'),
        ),
    ]
