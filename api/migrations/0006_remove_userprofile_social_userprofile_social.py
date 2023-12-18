# Generated by Django 5.0 on 2023-12-17 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_social_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='social',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='social',
            field=models.ManyToManyField(null=True, to='api.social'),
        ),
    ]
