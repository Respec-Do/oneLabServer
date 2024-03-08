import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('member_email', models.CharField(max_length=50)),
                ('member_password', models.CharField(max_length=20)),
                ('member_name', models.CharField(max_length=100)),
                ('member_phone', models.CharField(max_length=100)),
                ('member_status', models.BooleanField(default=True)),
                ('member_type', models.TextField(default='oneLabProject')),
            ],
            options={
                'db_table': 'tbl_member',
            },
        ),
    ]