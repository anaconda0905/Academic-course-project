# Generated by Django 2.2.3 on 2019-08-27 09:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('schools', '0002_auto_20190817_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='media/Users/avatar/%Y/%m/%d'),
        ),
    ]