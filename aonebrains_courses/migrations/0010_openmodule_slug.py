# Generated by Django 2.2.3 on 2019-09-14 17:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('aonebrains_courses', '0009_auto_20190911_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='openmodule',
            name='slug',
            field=models.SlugField(editable=False, max_length=200, null=True, unique=True),
        ),
    ]
