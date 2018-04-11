# Generated by Django 2.0.3 on 2018-03-30 11:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20180330_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='published',
            field=models.DateField(default=datetime.datetime(2018, 3, 30, 11, 31, 23, 99393, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
