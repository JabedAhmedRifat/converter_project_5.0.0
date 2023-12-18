import os
import tempfile
from django.shortcuts import redirect, render
from django.contrib.sites.shortcuts import get_current_site
from PIL import Image

def image_compressor(request):
    if request.method == 'POST':
        original_image = request.FILES.get('original_image')
        output_format = request.POST.get('output_format')  # Add a form field to specify the output format

        if original_image and output_format:
            try:
                # Create a temporary folder for compression
                temp_folder_path = tempfile.mkdtemp(prefix='temp_compression_', dir='media')

                # Save the original file in the temporary folder with a unique name
                original_file_name = "original"
                original_file_path = os.path.join(temp_folder_path, original_file_name)

                with open(original_file_path, 'wb+') as destination:
                    for chunk in original_image.chunks():
                        destination.write(chunk)

                # Compress the image and save the compressed file
                compressed_file_name = f"compressed.{output_format}"
                compressed_file_path = os.path.join('media', compressed_file_name)

                # Open the original image
                with Image.open(original_file_path) as img:
                    # Save the compressed image with optimization
                    img.save(compressed_file_path, format=output_format, quality=85, optimize=True)

                # Clean up the temporary folder
                os.remove(original_file_path)
                os.rmdir(temp_folder_path)

                # Generate the download link using Django's reverse function
                current_site = get_current_site(request)
                download_link = f'{request.scheme}://{current_site.domain}/media/{compressed_file_name}'

                request.session['download_link'] = download_link

                # Render the template with the compressed file link
                return redirect('image_result_page')

            except Exception as e:
                print(f"Error during image compression: {e}")

    else:
        print("Missing original_image or output_format in the form data")

    return render(request, 'image_compressor/converter.html')



def image_comprosser_result_page(request):
    download_link = request.session.pop('download_link', None)

    return render(request, 'image_compressor/result_page.html', {'download_link': download_link})