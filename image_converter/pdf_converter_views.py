import os
import tempfile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.base import ContentFile
from PIL import Image
import shutil
import fitz  # PyMuPDF
import zipfile

def pdf_converter(request):
    if request.method == 'POST':
        pdf_file = request.FILES['pdf_file']
        format_to = request.POST['image_format']

        if pdf_file and format_to:
            try:
                # Create a temporary folder for conversion
                temp_folder_path = tempfile.mkdtemp(prefix='temp_conversion_', dir='media')

                # Save the original file in the temporary folder with a unique name
                original_file_name = f"original_{pdf_file.name}"
                original_file_path = os.path.join(temp_folder_path, original_file_name)

                with open(original_file_path, 'wb+') as destination:
                    for chunk in pdf_file.chunks():
                        destination.write(chunk)

                # Convert PDF to images using PyMuPDF (MuPDF)
                pdf_document = fitz.open(original_file_path)
                for page_number in range(pdf_document.page_count):
                    page = pdf_document[page_number]
                    pixmap = page.get_pixmap()

                    # Convert Pixmap to PIL Image
                    image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

                    # Save the image
                    image_path = os.path.join(temp_folder_path, f"page_{page_number + 1}.png")
                    image.save(image_path, format="PNG")

                # Close the PDF document
                pdf_document.close()

                # Clean up the original PDF file
                os.remove(original_file_path)

                # Create the folder path for the converted images
                converted_images_folder_name = f"converted_images_folder_{format_to}"
                converted_images_folder_path = os.path.join('media', converted_images_folder_name)

                # Move the folder with the converted images to the media directory
                shutil.move(temp_folder_path, converted_images_folder_path)

                # Create a ZIP archive
                zip_file_path = os.path.join('media', f"{converted_images_folder_name}.zip")
                with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
                    for root, _, files in os.walk(converted_images_folder_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, converted_images_folder_path)
                            zip_file.write(file_path, arcname=arcname)

                # Generate the download link using Django's reverse function
                download_link = request.build_absolute_uri(f'/media/{converted_images_folder_name}.zip')

                request.session['download_link'] = download_link

                # Render the template with the converted file link
                return redirect('pdf_result_page')

            except Exception as e:
                print(f"Error during PDF conversion: {e}")

    else:
        print("Missing pdf_file or image_format in the form data")

    return render(request, 'pdf_converter/converter.html')


def pdf_result_page(request):
    download_link = request.session.pop('download_link', None)

    return render(request, 'pdf_converter/result_page.html', {'download_link': download_link})



















































# import os
# import tempfile
# from django.shortcuts import render, redirect
# from django.core.files.uploadedfile import InMemoryUploadedFile
# from PIL import Image
# import shutil
# import fitz  # PyMuPDF

# def pdf_converter(request):
#     if request.method == 'POST':
#         pdf_file = request.FILES['pdf_file']
#         format_to = request.POST['image_format']

#         if pdf_file and format_to:
#             try:
#                 # Create a temporary folder for conversion
#                 temp_folder_path = tempfile.mkdtemp(prefix='temp_conversion_', dir='media')

#                 # Save the original file in the temporary folder with a unique name
#                 original_file_name = f"original_{pdf_file.name}"
#                 original_file_path = os.path.join(temp_folder_path, original_file_name)

#                 with open(original_file_path, 'wb+') as destination:
#                     for chunk in pdf_file.chunks():
#                         destination.write(chunk)

#                 # Convert PDF to images using PyMuPDF (MuPDF)
#                 pdf_document = fitz.open(original_file_path)
#                 for page_number in range(pdf_document.page_count):
#                     page = pdf_document[page_number]
#                     pixmap = page.get_pixmap()

#                     # Convert Pixmap to PIL Image
#                     image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)

#                     # Save the image
#                     image_path = os.path.join(temp_folder_path, f"page_{page_number + 1}.png")
#                     image.save(image_path, format="PNG")

#                 # Close the PDF document
#                 pdf_document.close()

#                 # Clean up the original PDF file
#                 os.remove(original_file_path)

#                 # Create the folder path for the converted images
#                 #-------------------------------------------------------------------------------------------
#                 converted_images_folder_name = f"converted_images_folder_{format_to}"
#                 converted_images_folder_path = os.path.join('media', converted_images_folder_name)

#                 # Move the folder with the converted images to the media directory
#                 shutil.move(temp_folder_path, converted_images_folder_path)

#                 # Generate the download link using Django's reverse function
#                 download_link = request.build_absolute_uri(f'/media/{converted_images_folder_name}')

#                 request.session['download_link'] = download_link

#                 # Render the template with the converted file link
#                 return redirect('pdf_result_page')

#             except Exception as e:
#                 print(f"Error during PDF conversion: {e}")

#     else:
#         print("Missing pdf_file or image_format in the form data")

#     return render(request, 'pdf_converter/converter.html')

































# import os
# import tempfile
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.template.loader import render_to_string
# from django.core.files.uploadedfile import InMemoryUploadedFile
# from pdf2image import convert_from_path
# import shutil

# def pdf_converter(request):
#     if request.method == 'POST':
#         pdf_file = request.FILES['pdf_file']
#         format_to = request.POST['image_format']

#         if pdf_file and format_to:
#             try:
#                 # Create a temporary folder for conversion
#                 temp_folder_path = tempfile.mkdtemp(prefix='temp_conversion_', dir='media')

#                 # Save the original file in the temporary folder with a unique name
#                 original_file_name = f"original_{pdf_file.name}"
#                 original_file_path = os.path.join(temp_folder_path, original_file_name)

#                 with open(original_file_path, 'wb+') as destination:
#                     for chunk in pdf_file.chunks():
#                         destination.write(chunk)

#                 # Convert PDF to images
#                 images = convert_from_path(original_file_path)

#                 # Create a folder to store images
#                 converted_images_folder_path = os.path.join(temp_folder_path, 'converted_images_folder')
#                 os.makedirs(converted_images_folder_path)

#                 # Save images to the folder
#                 for i, image in enumerate(images):
#                     image_path = os.path.join(converted_images_folder_path, f"page_{i + 1}.png")
#                     image.save(image_path, 'PNG')

#                 # Clean up the original PDF file
#                 os.remove(original_file_path)

#                 # Create the folder path for the converted images
#                 converted_images_folder_name = f"converted_images_folder.{format_to}"
#                 converted_images_folder_path = os.path.join('media', converted_images_folder_name)

#                 # Move the folder with the converted images to the media directory
#                 shutil.move(converted_images_folder_path, os.path.join('media', converted_images_folder_name))

#                 # Generate the download link using Django's reverse function
#                 download_link = request.build_absolute_uri(f'/media/{converted_images_folder_name}')

#                 request.session['download_link'] = download_link

#                 # Render the template with the converted file link
#                 return redirect('pdf_result_page')

#             except Exception as e:
#                 print(f"Error during PDF conversion: {e}")

#     else:
#         print("Missing pdf_file or image_format in the form data")

#     return render(request, 'pdf_converter/converter.html')


def pdf_result_page(request):
    download_link = request.session.pop('download_link', None)

    return render(request, 'pdf_converter/result_page.html', {'download_link': download_link})
