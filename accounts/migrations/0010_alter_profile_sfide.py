# Generated by Django 4.2 on 2023-04-27 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_remove_profile_sfide_profile_sfide'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='sfide',
            field=models.ManyToManyField(blank=True, null=True, to='accounts.sfide'),
        ),
    ]