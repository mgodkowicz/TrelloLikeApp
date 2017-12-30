# Generated by Django 2.0 on 2017-12-29 19:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
                ('description', models.TextField()),
                ('priority', models.PositiveSmallIntegerField()),
                ('deadline', models.DateTimeField()),
                ('finished', models.BooleanField(default=False)),
                ('list_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='List', to='trello.List')),
                ('performer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Task', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProjectOwners',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProjectTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='contributors',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trello.UserProjectTeam'),
        ),
        migrations.AddField(
            model_name='project',
            name='owner_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Owner', to='trello.UserProjectOwners'),
        ),
        migrations.AddField(
            model_name='list',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Project', to='trello.Project'),
        ),
        migrations.AddField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Task', to='trello.Task'),
        ),
    ]
