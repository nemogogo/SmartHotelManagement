# Generated by Django 2.0.5 on 2018-06-12 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0013_auto_20180613_0113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(default=8, on_delete=django.db.models.deletion.CASCADE, to='hotel.Customer', verbose_name='客人信息'),
        ),
    ]
