# Generated by Django 3.1 on 2020-08-19 19:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('member_profile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minutes_inactive', models.IntegerField()),
                ('color', models.IntegerField(choices=[(1, 'Aqua'), (2, 'Black'), (3, 'Blue'), (4, 'Brown'), (5, 'Green'), (6, 'Lime'), (7, 'Maroon'), (8, 'Olive'), (9, 'Orange'), (10, 'Pink'), (11, 'Purple'), (12, 'Red'), (13, 'White'), (14, 'Yellow'), (15, 'Gray'), (16, 'Beige')], default=15)),
                ('alliance_position', models.IntegerField(choices=[(5, 'Leader'), (4, 'Heir'), (3, 'Officer'), (2, 'Member'), (1, 'Applicant')], default=1)),
                ('offensive_war_count', models.IntegerField()),
                ('defensive_war_count', models.IntegerField()),
                ('score', models.FloatField()),
                ('turns_in_vm', models.IntegerField()),
                ('infrastructure', models.FloatField()),
                ('soldiers', models.IntegerField()),
                ('tanks', models.IntegerField()),
                ('aircraft', models.IntegerField()),
                ('ships', models.IntegerField()),
                ('war_policy', models.IntegerField(choices=[(1, 'Attrition'), (2, 'Turtle'), (3, 'Blitzkrieg'), (4, 'Fortress'), (5, 'MoneyBags'), (6, 'Pirate'), (7, 'Tactician'), (8, 'Guardian'), (9, 'Covert'), (10, 'Arcane')])),
                ('domestic_policy', models.IntegerField(choices=[(1, 'Manifest Destiny'), (2, 'Open Markets'), (3, 'Technological Advancement'), (4, 'Imperialism'), (5, 'Urbanization')])),
                ('continent', models.TextField(choices=[('North America', 'North America'), ('South America', 'South America'), ('Africa', 'Africa'), ('Europe', 'Europe'), ('Asia', 'Asia'), ('Australia', 'Australia'), ('Antarctica', 'Antarctica')])),
                ('city_count', models.IntegerField()),
                ('spies', models.IntegerField()),
                ('money', models.FloatField()),
                ('gasoline', models.FloatField()),
                ('munitions', models.FloatField()),
                ('steel', models.FloatField()),
                ('aluminum', models.FloatField()),
                ('uranium', models.FloatField()),
                ('food', models.FloatField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('member_id', models.ForeignKey(db_column='nation_id', on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='member_profile.profile', to_field='nation_id')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
