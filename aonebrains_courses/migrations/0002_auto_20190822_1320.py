# Generated by Django 2.2.3 on 2019-08-22 20:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0005_student'),
        ('aonebrains_courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='opencourse',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses',
                                    to='accounts.SuperAdmin'),
        ),
        migrations.AlterField(
            model_name='opencourse',
            name='school_students',
            field=models.ManyToManyField(related_name='courses_enrolled', to='schools.SchoolStudent'),
        ),
        migrations.AlterField(
            model_name='opencourse',
            name='students',
            field=models.ManyToManyField(related_name='courses_joined', to='accounts.Student'),
        ),
        migrations.AlterField(
            model_name='opencourse',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses',
                                    to='aonebrains_courses.OpenSubject'),
        ),
        migrations.AlterField(
            model_name='openmodule',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modules',
                                    to='aonebrains_courses.OpenCourse'),
        ),
    ]
