# Generated by Django 5.0.2 on 2024-03-20 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('point', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='point_status',
            field=models.SmallIntegerField(choices=[(1, '충전'), (2, '사용'), (3, '적립')]),
        ),
    ]
