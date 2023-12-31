# Generated by Django 5.0 on 2023-12-14 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeline', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=50)),
                ('company_name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('assetsLink', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='SkillItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('K', 'Main skill'), ('O', 'Other skill')], max_length=1)),
            ],
        ),
    ]
