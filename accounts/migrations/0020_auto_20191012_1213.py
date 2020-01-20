# Generated by Django 2.2.3 on 2019-10-12 19:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0019_auto_20191009_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluser',
            name='avatar',
            field=models.TextField(blank=True, default='avatar/default_avatar.png', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='avatar/default_avatar.png', null=True,
                                    upload_to='media/Users/avatar/%Y/%m/%d'),
        ),
    ]