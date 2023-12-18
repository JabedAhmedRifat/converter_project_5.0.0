import os
import io
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import DocumentConversion
from django.shortcuts import get_object_or_404

from odf import text
from odf import teletype
from odf.opendocument import load

from pptx import Presentation
from pdf2docx import Converter as Pdf2DocxConverter
from fpdf import FPDF
from docx import Document as PyDocxDocument
# import unoconv
import pypandoc
from PyPDF2 import PdfFileReader
import openpyxl
import fitz  # PyMuPDF
# from pdf2pptx import convert_pdf

from docx2txt import process
from docx import Document
from io import BytesIO
from reportlab.pdfgen import canvas

import subprocess
import mammoth

from docx2pdf import convert

from django.http import HttpResponse
import docx2txt

from html2text import html2text
from bs4 import BeautifulSoup
import requests as r


from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter 

# import os
# os.environ["WEASYPRINT_BACKEND"] = "dummy"
# from weasyprint import HTML
import os.path

def document_converter(request):

    converted_document = None
    format_extension = None

    if request.method == 'POST':
        original_document = request.FILES['original_document']
        format_to = request.POST['document_format']

        # Save the original document details to the database
        if original_document and format_to:
            conversion = DocumentConversion(original_document=original_document, 
                                        original_document_name=original_document.name
            )
        
            conversion.save()




        # Get the path for the uploaded document
        original_document_path = os.path.join('media', str(conversion.original_document))
        original_document_format = original_document_path.split('.')[-1]





        try:
            



            # Conversion logic for different formats
            if original_document_format == 'docx' and format_to == 'pdf':
                dir_name, file_name = os.path.split(original_document_path)

                # Remove the file extension from the filename
                base_name, _ = os.path.splitext(file_name)

                # Create the full path for the PDF file in the same directory
                pdf_path = os.path.join(dir_name, f"{base_name}.pdf")

                try:
                    # Read DOCX file and convert to PDF
                    doc = Document(original_document_path)

                    # Create PDF file directly without reading
                    pdf = canvas.Canvas(pdf_path, pagesize=letter)

                    # Set font and size
                    pdf.setFont("Helvetica", 12)

                    # Adjust coordinates based on your requirements
                    x, y = 100, 800

                    # Iterate through paragraphs in DOCX and write to PDF
                    for paragraph in doc.paragraphs:
                        pdf.drawString(x, y, paragraph.text)
                        # You may need to adjust the coordinates based on your requirements
                        y -= 12  # Move to the next line

                    # Save PDF
                    pdf.save()

                    print(f"Conversion complete. PDF saved at: {pdf_path}")

                    # Optionally, set the converted document data and format extension
                    converted_document_data = None
                    format_extension = 'pdf'

                except Exception as e:
                    print(f"Error during DOCX to PDF conversion: {e}")
                    converted_document_data = None
                    format_extension = None
                    # Handle the error as needed

                # Optionally, remove the temporary PDF file
                # os.remove(pdf_path)
                            




            elif original_document_format == 'docx' and format_to == 'html':
                # Convert docx to html using mammoth
                original_document_data.seek(0)


                try:
                    result = mammoth.convert_to_html(io.BytesIO(original_document_content))
                    converted_document_data = result.value.encode('utf-8')
                except Exception as e:
                    print(f"Error during additional conversion: {e}")

                format_extension = 'html'






            # Add more conversion options as needed

            conversion.conversion_status = True
            conversion.format = format_to
            conversion.save()

            try:
                # Get the original document name without the file extension
                original_document_name = os.path.splitext(original_document.name)[0]

                converted_document = DocumentConversion(
                    original_document=original_document,
                    original_document_name=original_document_name,
                    conversion_status=True,
                    format=format_to
                )

                converted_document_path = f'{original_document_name}_{format_to}.{format_extension or "unknown"}'

                conversion.converted_document.save(
                    converted_document_path,
                    converted_document_data, save=True
                )

            except Exception as e:
                print(f"Error during additional conversion :{e}")
        except:
            print("Error during  conversion")

    else:
        print("Missing original_document or selected_format in the form data")

    # Retrieve conversion history for displaying on the page
    conversions = DocumentConversion.objects.all()
    context = {'conversions': conversions, 'converted_document': converted_document}
    return render(request, 'document_converter/converter.html', context)


def download_document(request, document_id):
    conversion = get_object_or_404(DocumentConversion, id=document_id)

    if conversion.converted_document:
        file_path = conversion.converted_document.path
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')  # Change content_type based on the format
            response['Content-Disposition'] = f'attachment; filename={conversion.original_document_name}.{conversion.format}'
            return response

    return HttpResponse("Document not found", status=404)