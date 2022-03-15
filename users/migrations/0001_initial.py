# Generated by Django 4.0.3 on 2022-03-15 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=20)),
                ('kakao_id', models.BigIntegerField(unique=True)),
                ('profile_image_url', models.URLField()),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
