# Generated by Django 5.0 on 2023-12-17 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_userprofile_social'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(max_length=11, null=True),
        ),
    ]
