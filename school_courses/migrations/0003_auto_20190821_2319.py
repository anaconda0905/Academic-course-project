# Generated by Django 2.2.3 on 2019-08-22 06:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('school_courses', '0002_auto_20190817_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_related',
                                    to='schools.Teacher'),
        ),
        migrations.AlterField(
            model_name='image',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_related',
                                    to='schools.Teacher'),
        ),
        migrations.AlterField(
            model_name='text',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_related',
                                    to='schools.Teacher'),
        ),
        migrations.AlterField(
            model_name='video',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_related',
                                    to='schools.Teacher'),
        ),
    ]
