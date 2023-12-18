# Generated by Django 5.0 on 2023-12-18 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_converter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveConversion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_folder', models.FileField(upload_to='archive_uploads/')),
                ('original_folder_name', models.CharField(blank=True, max_length=255, null=True)),
                ('conversion_status', models.BooleanField(default=False)),
                ('format', models.CharField(blank=True, max_length=10, null=True)),
                ('converted_archive', models.FileField(blank=True, null=True, upload_to='converted_archives/')),
            ],
        ),
    ]
