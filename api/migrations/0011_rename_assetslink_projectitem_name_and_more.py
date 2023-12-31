# Generated by Django 5.0 on 2023-12-20 10:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_educationitem'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectitem',
            old_name='assetsLink',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='projectitem',
            old_name='company_name',
            new_name='role',
        ),
        migrations.RemoveField(
            model_name='projectitem',
            name='location',
        ),
        migrations.RemoveField(
            model_name='projectitem',
            name='position',
        ),
        migrations.RemoveField(
            model_name='projectitem',
            name='timeline',
        ),
        migrations.AddField(
            model_name='projectitem',
            name='image',
            field=models.CharField(default='img/sample.jpg', max_length=100),
        ),
        migrations.CreateModel(
            name='ExperienceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeline', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=50)),
                ('company_name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('assetsLink', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
