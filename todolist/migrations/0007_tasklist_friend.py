from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0006_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasklist',
            name='friend',
            field=models.CharField(default='', max_length=200),
        ),
    ]
