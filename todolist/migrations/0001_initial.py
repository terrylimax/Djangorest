from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('completed', models.BooleanField(default=False)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('date_modified', models.DateField(auto_now=True)),
                ('priority', models.CharField(choices=[('h', 'High'), ('m', 'Medium'), ('l', 'Low'), ('n', 'None')], default='n', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Tasklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='tasklist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='todolist.Tasklist'),
        ),
    ]
