# Generated by Django 5.0.2 on 2024-03-13 10:20

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('file', '0001_initial'),
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('review_content', models.TextField()),
                ('review_rating', models.FloatField(default=0.0)),
                ('review_post_status', models.BooleanField(default=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='member.member')),
            ],
            options={
                'db_table': 'tbl_review',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='ReviewFile',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to='file.file')),
                ('path', models.ImageField(upload_to='review/%Y/%m/%d')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='review.review')),
            ],
            options={
                'db_table': 'tbl_review_file',
            },
        ),
    ]
