# Generated by Django 2.2.3 on 2019-08-17 07:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(editable=False, max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'class',
                'verbose_name_plural': 'classes',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('user',
                 models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='school_profile',
                                      to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                            related_name='teacher_class', to='schools.Grade')),
                ('school',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teachers',
                                   to='schools.School')),
                ('user',
                 models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_profile',
                                      to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SchoolStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students',
                                             to='schools.School')),
                ('teacher', models.ManyToManyField(related_name='students', to='schools.Teacher')),
                ('user',
                 models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student_profile',
                                      to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
