# Generated by Django 5.0 on 2023-12-13 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AudioConversion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_audio', models.FileField(upload_to='original_audios/')),
                ('original_audio_name', models.CharField(max_length=255)),
                ('conversion_status', models.BooleanField(default=False)),
                ('format', models.CharField(max_length=10)),
                ('converted_audio', models.FileField(blank=True, null=True, upload_to='converted_audios/')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentConversion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_document', models.FileField(upload_to='original_documents/')),
                ('original_document_name', models.CharField(max_length=255)),
                ('conversion_status', models.BooleanField(default=False)),
                ('format', models.CharField(blank=True, max_length=10, null=True)),
                ('converted_document', models.FileField(blank=True, null=True, upload_to='converted_documents/')),
            ],
        ),
        migrations.CreateModel(
            name='ImageConversion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_image', models.ImageField(upload_to='images/')),
                ('original_image_name', models.CharField(max_length=255)),
                ('converted_image', models.ImageField(blank=True, null=True, upload_to='converted_images/')),
                ('conversion_status', models.BooleanField(default=False)),
                ('format', models.CharField(blank=True, max_length=5, null=True)),
            ],
        ),
    ]
