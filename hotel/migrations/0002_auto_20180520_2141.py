# Generated by Django 2.0.5 on 2018-05-20 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='times',
            field=models.PositiveIntegerField(default=0, verbose_name='入住次数'),
        ),
    ]