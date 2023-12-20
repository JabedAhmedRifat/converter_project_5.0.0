import os
import tempfile
from django.shortcuts import redirect, render
from wand.image import Image as WandImage
from django.contrib.sites.shortcuts import get_current_site

def image_converter(request):
    if request.method == 'POST':
        original_image = request.FILES['original_image']
        format_to = request.POST['image_format']

        if original_image and format_to:
            try:
                # Create a temporary folder for conversion
                temp_folder_path = tempfile.mkdtemp(prefix='temp_conversion_', dir='media')

                # Save the original file in the temporary folder with a unique name
                original_file_name = f"original.{format_to}"
                original_file_path = os.path.join(temp_folder_path, original_file_name)

                with open(original_file_path, 'wb+') as destination:
                    for chunk in original_image.chunks():
                        destination.write(chunk)

                # Convert the image using Wand
                with WandImage(filename=original_file_path) as img:
                    # Resize only for ICO format
                    if format_to.lower() == 'ico':
                        img.resize(256, 256)  # Adjust the dimensions as needed

                    # Ensure the format is lowercase
                    format_to = format_to.lower()
                    converted_file_name = f"converted.{format_to}"
                    converted_image_path = os.path.join('media', converted_file_name)
                    img.save(filename=converted_image_path)

                # Clean up the temporary folder
                os.remove(original_file_path)
                os.rmdir(temp_folder_path)

                # Generate the download link using Django's reverse function
                current_site = get_current_site(request)
                download_link = f'{request.scheme}://{current_site.domain}/media/{converted_file_name}'

                request.session['download_link'] = download_link

                # Render the template with the converted file link
                return redirect('image_result_page')

            except Exception as e:
                print(f"Error during image conversion: {e}")

    else:
        print("Missing original_image or image_format in the form data")

    return render(request, 'image_converter/converter.html')

def image_result_page(request):
    download_link = request.session.pop('download_link', None)

    return render(request, 'image_converter/result_page.html', {'download_link': download_link})

















































# import os
# import tempfile
# from django.shortcuts import redirect, render
# from PIL import Image
# from django.contrib.sites.shortcuts import get_current_site

# def image_converter(request):
#     if request.method == 'POST':
#         original_image = request.FILES['original_image']
#         format_to = request.POST['image_format']

#         if original_image and format_to:
#             try:
#                  # Create a temporary folder for conversion
#                 temp_folder_path = tempfile.mkdtemp(prefix='temp_conversion_', dir='media')

#                 # Save the original file in the temporary folder with a unique name
#                 original_file_name = f"original.{format_to}"
#                 original_file_path = os.path.join(temp_folder_path, original_file_name)

#                 with open(original_file_path, 'wb+') as destination:
#                     for chunk in original_image.chunks():
#                         destination.write(chunk)

#                 # Open the original image to get its format
#                 with Image.open(original_file_path) as img:
#                     original_format = img.format.lower()

#                     # Convert and save the image to the desired format
#                     converted_file_name = f"converted.{format_to}"
#                     converted_image_path = os.path.join('media', converted_file_name)
#                     img.save(converted_image_path, format=format_to.upper())  # Ensure the format is uppercase

#                 # Clean up the temporary folder
#                 os.remove(original_file_path)
#                 os.rmdir(temp_folder_path)

#                 # Generate the download link using Django's reverse function
#                 current_site = get_current_site(request)
#                 download_link = f'{request.scheme}://{current_site.domain}/media/{converted_file_name}'

#                 request.session['download_link'] = download_link

#                 # Render the template with the converted file link
#                 return redirect('image_result_page')

#             except Exception as e:
#                 print(f"Error during image conversion: {e}")

#     else:
#         print("Missing original_image or image_format in the form data")

#     return render(request, 'image_converter/converter.html')

# def image_result_page(request):
#     download_link = request.session.pop('download_link', None)

#     return render(request, 'image_converter/result_page.html', {'download_link': download_link})
