# Generated by Django 2.2.3 on 2019-10-13 17:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('school_courses', '0011_auto_20191007_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalschoolcourse',
            name='preview',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='schoolcourse',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='courses/preview/'),
        ),
    ]
