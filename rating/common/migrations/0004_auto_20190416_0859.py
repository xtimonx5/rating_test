# Generated by Django 2.2 on 2019-04-16 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_leaderboard'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='raterecord',
            index=models.Index(fields=['-rating', 'datetime'], name='common_rate_rating_3e88d6_idx'),
        ),
    ]