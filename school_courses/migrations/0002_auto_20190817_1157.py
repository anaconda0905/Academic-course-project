# Generated by Django 2.2.3 on 2019-08-17 18:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('school_courses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolcourse',
            name='grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='grade', to='accounts.Grade'),
        ),
    ]
