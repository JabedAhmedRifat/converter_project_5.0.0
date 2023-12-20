import os
import tempfile
from django.shortcuts import redirect, render
import subprocess
from django.contrib.sites.shortcuts import get_current_site
import shutil



def convert_document(input_path, output_path, output_format):
    try:
        # Use the absolute path for unoconv
        unoconv_path = shutil.which('unoconv')
        subprocess.run([unoconv_path, "-f", output_format, "-o", output_path, input_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during document conversion: {e}")

def document_converter(request):
    if request.method == 'POST':
        original_file = request.FILES.get('original_file')
        format_to = request.POST.get('output_format')

        print(f"Original file: {original_file}")
        print(f"Format to: {format_to}")

        if original_file and format_to:
            temp_folder_path = None
            original_file_path = None
            converted_file_path = None

            try:
                # Create a temporary folder for conversion
                temp_folder_path = tempfile.mkdtemp(prefix='temp_conversion_', dir='media')

                # Save the original file in the temporary folder with a unique name
                original_file_name = f"original.{original_file.name.split('.')[-1]}"
                original_file_path = os.path.join(temp_folder_path, original_file_name)

                print(f"Original file path: {original_file_path}")

                with open(original_file_path, 'wb+') as destination:
                    for chunk in original_file.chunks():
                        destination.write(chunk)

                # Convert the document to the desired format using unoconv
                converted_file_name = f"converted.{format_to}"
                converted_file_path = os.path.join('media', converted_file_name)

                print(f"Converted file path: {converted_file_path}")

                convert_document(original_file_path, converted_file_path, format_to)

                # Generate the download link using Django's reverse function
                current_site = get_current_site(request)
                download_link = f'{request.scheme}://{current_site.domain}/media/{converted_file_name}'

                request.session['download_link'] = download_link

                # Render the template with the converted file link
                return redirect('document_result_page')

            except Exception as e:
                print(f"Error during document conversion: {e}")

            finally:
                # Clean up the temporary folder
                if original_file_path:
                    os.remove(original_file_path)
                if temp_folder_path:
                    os.rmdir(temp_folder_path)

    else:
        print("Missing original_file or output_format in the form data")

    return render(request, 'document_converter/converter.html')


def document_result_page(request):
    download_link = request.session.pop('download_link', None)

    return render(request, 'document_converter/result_page.html', {'download_link': download_link})

































































































# import os
# import tempfile
# from django.shortcuts import redirect, render
# import pypandoc
# from django.contrib.sites.shortcuts import get_current_site


# def document_converter(request):
#     if request.method == 'POST':
#         original_file = request.FILES['original_file']
#         format_to = request.POST['output_format']

#         if original_file and format_to:
#             try:
#                 # Create a temporary folder for conversion
#                 temp_folder_path = tempfile.mkdtemp(prefix='temp_conversion_', dir='media')

#                 # Save the original file in the temporary folder with a unique name
#                 original_file_name = f"original.{original_file.name.split('.')[-1]}"
#                 original_file_path = os.path.join(temp_folder_path, original_file_name)

#                 with open(original_file_path, 'wb+') as destination:
#                     for chunk in original_file.chunks():
#                         destination.write(chunk)

#                 # Convert the document to the desired format
#                 converted_file_name = f"converted.{format_to}"
#                 converted_file_path = os.path.join('media', converted_file_name)

#                 pypandoc.convert_file(original_file_path, format_to, outputfile=converted_file_path)

#                 # Clean up the temporary folder
#                 os.remove(original_file_path)
#                 os.rmdir(temp_folder_path)

#                 # Generate the download link using Django's reverse function
#                 current_site = get_current_site(request)
#                 download_link = f'{request.scheme}://{current_site.domain}/media/{converted_file_name}'

#                 request.session['download_link'] = download_link

#                 # Render the template with the converted file link
#                 return redirect('document_result_page')

#             except Exception as e:
#                 print(f"Error during document conversion: {e}")

#     else:
#         print("Missing original_file or output_format in the form data")

#     return render(request, 'document_converter/converter.html')

# def document_result_page(request):
#     download_link = request.session.pop('download_link', None)

#     return render(request, 'document_converter/result_page.html', {'download_link': download_link})
























# import os
# import io
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from .models import DocumentConversion
# from django.shortcuts import get_object_or_404

# from odf import text
# from odf import teletype
# from odf.opendocument import load

# from pptx import Presentation
# from pdf2docx import Converter as Pdf2DocxConverter
# from fpdf import FPDF
# from docx import Document as PyDocxDocument
# # import unoconv
# import pypandoc
# from PyPDF2 import PdfFileReader
# import openpyxl
# import fitz  # PyMuPDF
# # from pdf2pptx import convert_pdf

# from docx2txt import process
# from docx import Document
# from io import BytesIO
# from reportlab.pdfgen import canvas

# import subprocess
# import mammoth

# from docx2pdf import convert

# from django.http import HttpResponse
# import docx2txt

# from html2text import html2text
# from bs4 import BeautifulSoup
# import requests as r


# from docx import Document
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter 

# # import os
# # os.environ["WEASYPRINT_BACKEND"] = "dummy"
# # from weasyprint import HTML
# import os.path

# def document_converter(request):

#     converted_document = None
#     format_extension = None

#     if request.method == 'POST':
#         original_document = request.FILES['original_document']
#         format_to = request.POST['document_format']

#         # Save the original document details to the database
#         if original_document and format_to:
#             conversion = DocumentConversion(original_document=original_document, 
#                                         original_document_name=original_document.name
#             )
        
#             conversion.save()




#         # Get the path for the uploaded document
#         original_document_path = os.path.join('media', str(conversion.original_document))
#         original_document_format = original_document_path.split('.')[-1]





#         try:
            



#             # Conversion logic for different formats
#             if original_document_format == 'docx' and format_to == 'pdf':
#                 dir_name, file_name = os.path.split(original_document_path)

#                 # Remove the file extension from the filename
#                 base_name, _ = os.path.splitext(file_name)

#                 # Create the full path for the PDF file in the same directory
#                 pdf_path = os.path.join(dir_name, f"{base_name}.pdf")

#                 try:
#                     # Read DOCX file and convert to PDF
#                     doc = Document(original_document_path)

#                     # Create PDF file directly without reading
#                     pdf = canvas.Canvas(pdf_path, pagesize=letter)

#                     # Set font and size
#                     pdf.setFont("Helvetica", 12)

#                     # Adjust coordinates based on your requirements
#                     x, y = 100, 800

#                     # Iterate through paragraphs in DOCX and write to PDF
#                     for paragraph in doc.paragraphs:
#                         pdf.drawString(x, y, paragraph.text)
#                         # You may need to adjust the coordinates based on your requirements
#                         y -= 12  # Move to the next line

#                     # Save PDF
#                     pdf.save()

#                     print(f"Conversion complete. PDF saved at: {pdf_path}")

#                     # Optionally, set the converted document data and format extension
#                     converted_document_data = None
#                     format_extension = 'pdf'

#                 except Exception as e:
#                     print(f"Error during DOCX to PDF conversion: {e}")
#                     converted_document_data = None
#                     format_extension = None
#                     # Handle the error as needed

#                 # Optionally, remove the temporary PDF file
#                 # os.remove(pdf_path)
                            




#             elif original_document_format == 'docx' and format_to == 'html':
#                 # Convert docx to html using mammoth
#                 original_document_data.seek(0)


#                 try:
#                     result = mammoth.convert_to_html(io.BytesIO(original_document_content))
#                     converted_document_data = result.value.encode('utf-8')
#                 except Exception as e:
#                     print(f"Error during additional conversion: {e}")

#                 format_extension = 'html'






#             # Add more conversion options as needed

#             conversion.conversion_status = True
#             conversion.format = format_to
#             conversion.save()

#             try:
#                 # Get the original document name without the file extension
#                 original_document_name = os.path.splitext(original_document.name)[0]

#                 converted_document = DocumentConversion(
#                     original_document=original_document,
#                     original_document_name=original_document_name,
#                     conversion_status=True,
#                     format=format_to
#                 )

#                 converted_document_path = f'{original_document_name}_{format_to}.{format_extension or "unknown"}'

#                 conversion.converted_document.save(
#                     converted_document_path,
#                     converted_document_data, save=True
#                 )

#             except Exception as e:
#                 print(f"Error during additional conversion :{e}")
#         except:
#             print("Error during  conversion")

#     else:
#         print("Missing original_document or selected_format in the form data")

#     # Retrieve conversion history for displaying on the page
#     conversions = DocumentConversion.objects.all()
#     context = {'conversions': conversions, 'converted_document': converted_document}
#     return render(request, 'document_converter/converter.html', context)


# def download_document(request, document_id):
#     conversion = get_object_or_404(DocumentConversion, id=document_id)

#     if conversion.converted_document:
#         file_path = conversion.converted_document.path
#         with open(file_path, 'rb') as f:
#             response = HttpResponse(f.read(), content_type='application/octet-stream')  # Change content_type based on the format
#             response['Content-Disposition'] = f'attachment; filename={conversion.original_document_name}.{conversion.format}'
#             return response

#     return HttpResponse("Document not found", status=404)