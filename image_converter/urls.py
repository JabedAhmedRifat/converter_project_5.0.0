from django.urls import path
from .views import *
from .audio_views import *

from .document_views import *

from .archive_views import *

from .pdf_converter_views import *

from .bmp_converter_views import *

from .pdf_compress_views import *

from .image_compress_views import *

urlpatterns = [
    path('image-converter/', image_converter, name='image_converter'),
    path('download/<int:image_id>/', download_image, name='download_image'),


    path('audio-converter/', audio_converter, name='audio_converter'),
    path('download/<int:audio_id>/', download_audio, name='download_audio'),


    path('document-converter/', document_converter, name='document_converter'),
    path('download/<int:document_id>/', download_document, name='download_document'),
    
    path('archive-converter/', archive_converter, name='archive_converter'),
    path('result-page/', archive_result_page, name='archive_result_page'),
    
    
    path('pdf-converter/', pdf_converter, name='pdf_converter'),
    path('result-page/', pdf_result_page, name='pdf_result_page'),
    
    
    path('bmp-converter/', bmp_converter, name='bmp_converter'),
    path('result-page/', bmp_result_page, name='bmp_result_page'),
    
    path('pdf_compressor/', pdf_compressor, name='pdf_compressor'),
    path('result-page/', pdf_compresser_result_page, name='pdf_result_page'),
    
    
    path('image_compressor/', image_compressor, name='image_compressor'),
    path('result-page/', image_comprosser_result_page, name='image_result_page'),
]

