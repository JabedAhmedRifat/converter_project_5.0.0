import os
import tempfile
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from ebooklib import epub
from PIL import Image
from PyPDF2 import PdfFileReader

def ebook_converter(request):
    if request.method == 'POST':
        original_ebook = request.FILES['original_ebook']
        original_format = request.POST['original_format']
        format_to = request.POST['ebook_format']
        
        print(request.POST)
        print(request.FILES)


        if original_ebook and original_format and format_to:
            try:
                # Create a temporary folder for conversion
                temp_folder_path = tempfile.mkdtemp(prefix='temp_conversion_', dir='media')

                # Save the original file in the temporary folder with a unique name
                original_file_name = f"original.{original_format}"
                original_file_path = os.path.join(temp_folder_path, original_file_name)

                with open(original_file_path, 'wb+') as destination:
                    for chunk in original_ebook.chunks():
                        destination.write(chunk)

                # Convert the ebook to the desired format
                converted_file_name = f"converted.{format_to}"
                converted_file_path = os.path.join(temp_folder_path, converted_file_name)

                if original_format == 'epub' and format_to == 'pdf':
                    # Convert EPUB to PDF using ebooklib and PIL
                    book = epub.read_epub(original_file_path)
                    img = Image.new('RGB', (600, 800), (255, 255, 255))
                    img.save(converted_file_path, 'PDF', resolution=100.0)

                # Add more conversion cases based on original_format and format_to

                # Clean up the temporary folder
                os.remove(original_file_path)

                # Generate the download link using Django's reverse function
                current_site = get_current_site(request)
                download_link = f'{request.scheme}://{current_site.domain}/media/{converted_file_name}'

                request.session['download_link'] = download_link

                # Render the template with the converted file link
                return redirect('ebook_result_page')

            except Exception as e:
                print(f"Error during ebook conversion: {e}")

    else:
        print("Missing original_ebook, original_format, or ebook_format in the form data")

    return render(request, 'ebook_converter/converter.html')




def ebook_result_page(request):
    download_link = request.session.pop('download_link', None)

    return render(request, 'ebook_converter/result_page.html', {'download_link': download_link})