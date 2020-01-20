# Generated by Django 2.2.3 on 2019-09-25 01:12

import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models

import courses.fields


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0013_auto_20190923_2227'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aonebrains_courses', '0010_openmodule_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalOpenSubject',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(editable=False, max_length=200)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.TextField(null=True)),
                ('history_type',
                 models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Subject',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalOpenModule',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('order', courses.fields.OrderField(blank=True)),
                ('slug', models.SlugField(editable=False, max_length=200, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.TextField(null=True)),
                ('history_type',
                 models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('course', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                             on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                             to='aonebrains_courses.OpenCourse')),
                ('history_user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Module',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalOpenCourse',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('preview', models.TextField(max_length=100, null=True)),
                ('slug', models.SlugField(editable=False, max_length=200)),
                ('overview', models.TextField()),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.TextField(null=True)),
                ('history_type',
                 models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('admin', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                            on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                            to='accounts.SuperAdmin')),
                ('creator', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                              on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                              to='accounts.Curator')),
                ('grade', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                            on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                            to='accounts.Grade')),
                ('history_user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+',
                                   to=settings.AUTH_USER_MODEL)),
                ('subject', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                              on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                              to='aonebrains_courses.OpenSubject')),
            ],
            options={
                'verbose_name': 'historical Course',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalOpenContent',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('order', courses.fields.OrderField(blank=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.TextField(null=True)),
                ('history_type',
                 models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('content_type', models.ForeignKey(blank=True, db_constraint=False, limit_choices_to={
                    'model__in': ('atext', 'avideo', 'aimage', 'afile')}, null=True,
                                                   on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                                   to='contenttypes.ContentType')),
                ('history_user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+',
                                   to=settings.AUTH_USER_MODEL)),
                ('module', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                             on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                             to='aonebrains_courses.OpenModule')),
            ],
            options={
                'verbose_name': 'historical Content',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalAVideo',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('updated', models.DateTimeField(blank=True, editable=False)),
                ('file', models.TextField(max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.TextField(null=True)),
                ('history_type',
                 models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('creator', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                              on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                              to='accounts.Curator')),
                ('history_user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical AVideo',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalAText',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('updated', models.DateTimeField(blank=True, editable=False)),
                ('content', models.TextField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.TextField(null=True)),
                ('history_type',
                 models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('creator', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                              on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                              to='accounts.Curator')),
                ('history_user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical AText',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalAImage',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('updated', models.DateTimeField(blank=True, editable=False)),
                ('file', models.TextField(max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.TextField(null=True)),
                ('history_type',
                 models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('creator', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                              on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                              to='accounts.Curator')),
                ('history_user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical AImage',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalAFile',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('created', models.DateTimeField(blank=True, editable=False)),
                ('updated', models.DateTimeField(blank=True, editable=False)),
                ('file', models.TextField(max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.TextField(null=True)),
                ('history_type',
                 models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('creator', models.ForeignKey(blank=True, db_constraint=False, null=True,
                                              on_delete=django.db.models.deletion.DO_NOTHING, related_name='+',
                                              to='accounts.Curator')),
                ('history_user',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical AFile',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]