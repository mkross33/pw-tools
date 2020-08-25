# Generated by Django 3.1 on 2020-08-19 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('member_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AwardCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('category', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=128)),
                ('image', models.ImageField(upload_to='images/awards/')),
                ('recipients', models.ManyToManyField(to='member_profile.Profile')),
            ],
        ),
    ]
