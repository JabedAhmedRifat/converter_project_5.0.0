from django.db import models


class ImageConversion(models.Model):
    original_image = models.ImageField(upload_to='images/')
    original_image_name = models.CharField(max_length=255)
    converted_image = models.ImageField(upload_to='converted_images/', blank=True, null=True)
    conversion_status = models.BooleanField(default=False)
    format = models.CharField(max_length=5, blank=True, null=True)


class AudioConversion(models.Model):
    original_audio = models.FileField(upload_to='original_audios/')
    original_audio_name = models.CharField(max_length=255)
    conversion_status = models.BooleanField(default=False)
    format = models.CharField(max_length=10)
    converted_audio = models.FileField(upload_to='converted_audios/', null=True, blank=True)


class DocumentConversion(models.Model):
    original_document = models.FileField(upload_to='original_documents/')
    original_document_name = models.CharField(max_length=255)
    conversion_status = models.BooleanField(default=False)
    format = models.CharField(max_length=10, null=True, blank=True)
    converted_document = models.FileField(upload_to='converted_documents/', null=True, blank=True)
    
    
    
class ArchiveConversion(models.Model):
    original_folder = models.FileField(upload_to='archive_uploads/')
    original_folder_name = models.CharField(max_length=255, blank=True, null=True)
    conversion_status = models.BooleanField(default=False)
    format = models.CharField(max_length=10, null=True, blank=True)
    converted_archive = models.FileField(upload_to='converted_archives/', null=True, blank=True)
