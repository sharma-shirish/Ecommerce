# Generated by Django 2.2.28 on 2022-07-06 02:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coreshop', '0006_auto_20220705_1312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='start_date',
            new_name='start_date_time',
        ),
    ]
