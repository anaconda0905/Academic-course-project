# Generated by Django 2.2.3 on 2019-08-24 20:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('aonebrains_courses', '0003_auto_20190822_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opencourse',
            name='school_students',
            field=models.ManyToManyField(null=True, related_name='courses_enrolled', to='schools.SchoolStudent'),
        ),
        migrations.AlterField(
            model_name='opencourse',
            name='students',
            field=models.ManyToManyField(null=True, related_name='courses_joined', to='accounts.Student'),
        ),
    ]
