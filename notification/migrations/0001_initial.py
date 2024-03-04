# Generated by Django 5.0.2 on 2024-03-04 17:46

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('notification_title', models.CharField(max_length=30)),
                ('notification_content', models.CharField(max_length=2000)),
                ('notification_view_count', models.IntegerField(default=0)),
                ('notification_status', models.SmallIntegerField(choices=[(0, '커뮤니티'), (1, '원랩'), (2, '장소공유'), (3, '대회공모전')], default=0)),
            ],
            options={
                'db_table': 'tbl_notification',
                'ordering': ['-id'],
            },
        ),
    ]
