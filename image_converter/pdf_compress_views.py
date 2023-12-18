import os
import tempfile
from django.shortcuts import redirect, render
from PyPDF2 import PdfReader, PdfWriter
from django.contrib.sites.shortcuts import get_current_site

def pdf_compressor(request):
    if request.method == 'POST':
        original_pdf = request.FILES.get('original_pdf')

        if original_pdf:
            try:
                # Create a temporary folder for compression
                temp_folder_path = tempfile.mkdtemp(prefix='temp_compression_', dir='media')

                # Save the original file in the temporary folder with a unique name
                original_file_name = "original.pdf"
                original_file_path = os.path.join(temp_folder_path, original_file_name)

                with open(original_file_path, 'wb+') as destination:
                    for chunk in original_pdf.chunks():
                        destination.write(chunk)

                # Compress the PDF and save the compressed file
                compressed_file_name = "compressed.pdf"
                compressed_file_path = os.path.join('media', compressed_file_name)

                with open(original_file_path, 'rb') as original_file:
                    pdf_reader = PdfReader(original_file)
                    pdf_writer = PdfWriter()

                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)

                    with open(compressed_file_path, 'wb') as compressed_file:
                        pdf_writer.write(compressed_file)

                # Clean up the temporary folder
                os.remove(original_file_path)
                os.rmdir(temp_folder_path)

                # Generate the download link using Django's reverse function
                current_site = get_current_site(request)
                download_link = f'{request.scheme}://{current_site.domain}/media/{compressed_file_name}'

                request.session['download_link'] = download_link

                # Render the template with the compressed file link
                return redirect('pdf_result_page')

            except Exception as e:
                print(f"Error during PDF compression: {e}")

    else:
        print("Missing original_pdf in the form data")

    return render(request, 'pdf_compressor/converter.html')


def pdf_compresser_result_page(request):
    download_link = request.session.pop('download_link', None)

    return render(request, 'pdf_compressor/result_page.html', {'download_link': download_link})




















# import os
# import tempfile
# from django.shortcuts import redirect, render
# from PyPDF2 import PdfReader, PdfWriter
# from django.contrib.sites.shortcuts import get_current_site

# def pdf_compressor(request):
#     if request.method == 'POST':
#         original_pdf = request.FILES['original_pdf']

#         if original_pdf:
#             try:
#                 # Create a temporary folder for compression
#                 temp_folder_path = tempfile.mkdtemp(prefix='temp_compression_', dir='media')

#                 # Save the original file in the temporary folder with a unique name
#                 original_file_name = "original.pdf"
#                 original_file_path = os.path.join(temp_folder_path, original_file_name)

#                 with open(original_file_path, 'wb+') as destination:
#                     for chunk in original_pdf.chunks():
#                         destination.write(chunk)

#                 # Compress the PDF and save the compressed file
#                 compressed_file_name = "compressed.pdf"
#                 compressed_file_path = os.path.join('media', compressed_file_name)

#                 with open(original_file_path, 'rb') as original_file:
#                     pdf_reader = PdfReader(original_file)
#                     pdf_writer = PdfWriter()

#                     for page_num in range(pdf_reader.pages):
#                         pdf_writer.addPage(pdf_reader.getPage(page_num))

#                     with open(compressed_file_path, 'wb') as compressed_file:
#                         pdf_writer.write(compressed_file)

#                 # Clean up the temporary folder
#                 os.remove(original_file_path)
#                 os.rmdir(temp_folder_path)

#                 # Generate the download link using Django's reverse function
#                 current_site = get_current_site(request)
#                 download_link = f'{request.scheme}://{current_site.domain}/media/{compressed_file_name}'

#                 request.session['download_link'] = download_link

#                 # Render the template with the compressed file link
#                 return redirect('result_page')

#             except Exception as e:
#                 print(f"Error during PDF compression: {e}")

#     else:
#         print("Missing original_pdf in the form data")

#     return render(request, 'pdf_compressor/converter.html')


# def result_page(request):
#     download_link = request.session.pop('download_link', None)

#     return render(request, 'pdf_compressor/result_page.html', {'download_link': download_link})
