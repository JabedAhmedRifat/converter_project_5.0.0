import os
import io
from PIL import Image
# from wand.image import Image as WandImage--------later
# import pyvips---later
from django.shortcuts import render, redirect
from .models import ImageConversion
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

import imageio
import io
# import wbmpimage

# import aspose.words as aw---------later 


def image_converter(request):

    converted_image = None
    format_extension = None

    if request.method == 'POST':
        original_image = request.FILES['original_image']
        format_to = request.POST['image_format']

        # Save the original image details to the database
        conversion = ImageConversion(original_image=original_image, original_image_name=original_image.name)
        conversion.save()

        # Get the path for the uploaded image
        original_image_path = os.path.join('media', str(conversion.original_image))
        original_image_format = original_image_path.split('.')[-1]

        # Convert the image using different libraries for different formats
        with open(original_image_path, 'rb') as img_file:
            original_image_data = io.BytesIO(img_file.read())
            original_image_pil = Image.open(original_image_data)
            converted_image_data = io.BytesIO()

            

            # Conversion logic for different formats
            if original_image_format == 'png' and format_to == 'bmp':
                original_image_pil.save(converted_image_data, format='BMP')
                format_extension = 'bmp'

            elif original_image_format == 'png' and format_to == 'gif':
                original_image_pil.save(converted_image_data, format='GIF')
                format_extension = 'gif'

            elif original_image_format == 'png' and format_to == 'jpg':
                original_image_pil.save(converted_image_data, format='JPEG')
                format_extension = 'jpg'

            elif original_image_format == 'png' and format_to == 'webp':
                original_image_pil.save(converted_image_data, format='WEBP')
                format_extension = 'webp'


            # -----error-----------
            elif original_image_format == 'svg' and format_to == 'png':
                # Use Wand to convert SVG to PNG
                with WandImage(file=original_image_path, format="svg") as img:
                    img.format = 'png'
                    img.save(file=converted_image_data)
                
                # Reset the position of the BytesIO object before opening with Pillow
                converted_image_data.seek(0)
                
                # Open the converted PNG file with Pillow
                original_image_pil = Image.open(converted_image_data)
                format_extension = 'png'

                
            elif original_image_format == 'tga' and format_to == 'png':
                # Read the TGA image using imageio
                original_image_data = imageio.imread(original_image_path)

                # Create an in-memory stream for the converted image
                converted_image_data = io.BytesIO()

                # Save the image in PNG format
                imageio.imwrite(converted_image_data, original_image_data, format='PNG')

                # Reset the position of the BytesIO object before using it
                converted_image_data.seek(0)

                format_extension = 'png'




            elif original_image_format == 'gif' and format_to == 'png':
                original_image_pil.save(converted_image_data, format='PNG')
                format_extension = 'png'

            elif original_image_format == 'gif' and format_to == 'jpg':
                # Convert GIF to RGB mode (remove alpha channel) for JPG format
                original_image_pil = original_image_pil.convert('RGB')
                original_image_pil.save(converted_image_data, format='JPEG')
                format_extension = 'jpg'

            elif original_image_format == 'jpg' and format_to == 'gif':
                original_image_pil.save(converted_image_data, format='GIF')
                format_extension = 'gif'

            elif original_image_format == 'bmp' and format_to == 'jpg':
                original_image_pil.save(converted_image_data, format='JPEG')
                format_extension = 'jpg'


            elif original_image_format == 'jpg' and format_to == 'webp':
                original_image_pil.save(converted_image_data, format='WEBP')
                format_extension = 'webp'

            elif original_image_format == 'webp' and format_to == 'jpg':
                original_image_pil.save(converted_image_data, format='JPEG')
                format_extension = 'jpg'


            elif original_image_format == 'tiff' and format_to == 'jpg':
                original_image_pil.save(converted_image_data, format='JPEG')
                format_extension = 'jpg'


            elif original_image_format == 'jpg' and format_to == 'tiff':
                original_image_pil.save(converted_image_data, format='TIFF')
                format_extension = 'tiff'


            elif original_image_format == 'png' and format_to == 'eps':
                original_image_pil = original_image_pil.convert('RGB')
                original_image_pil.save(converted_image_data, format='EPS')
                format_extension = 'eps'

            elif original_image_format == 'ico' and format_to == 'png':
                original_image_pil.save(converted_image_data, format='PNG')
                format_extension = 'png'


            elif original_image_format == 'ico' and format_to == 'jpg':
                original_image_pil = original_image_pil.convert('RGB')
                original_image_pil.save(converted_image_data, format='JPEG')
                format_extension = 'jpg'


            elif original_image_format == 'ico' and format_to == 'webp':
                original_image_pil.save(converted_image_data, format='WEBP')
                format_extension = 'webp'

            elif original_image_format == 'bmp' and format_to == 'gif':
                original_image_pil.save(converted_image_data, format='GIF')
                format_extension = 'gif'

            elif original_image_format == 'png' and format_to == 'ico':
                original_image_pil.save(converted_image_data, format='ICO')
                format_extension = 'ico'


            elif original_image_format == 'jpg' and format_to == 'ico':
                original_image_pil.save(converted_image_data, format='ICO')
                format_extension = 'ico'
            

            elif original_image_format == 'tga' and format_to == 'png':
                image = pyvips.Image.new_from_file(original_image_path)
                image.write_to_buffer('.png', target=converted_image_data)
                format_extension = 'png'


            elif original_image_format == 'tiff' and format_to == 'png':
                original_image_pil.save(converted_image_data, format='PNG')
                format_extension = 'png'


            elif original_image_format == 'bmp' and format_to == 'webp':
                original_image_pil.save(converted_image_data, format='WEBP')
                format_extension = 'webp'

            elif original_image_format == 'wbmp' and format_to == 'png':
                img = imageio.imread(original_image_path, format='wbmp')
                pil_image = Image.fromarray(img)
                pil_image = pil_image.convert('RGB')
                converted_image_data = io.BytesIO()
                pil_image.save(converted_image_data, format='PNG')
                converted_image_data.seek(0)
                format_extension = 'png'

            # Add more conversion options as needed

            
            # converted_image_path = f'{original_image.name.split(".")[0]}_{format_to}.{format_extension}'
            # conversion.converted_image.save(
            #     converted_image_path,
            #     converted_image_data, save=False
            # )

            conversion.conversion_status = True
            conversion.format = format_to
            conversion.save()

            try:
                # Get the original image name without the file extension
                original_image_name = os.path.splitext(original_image.name)[0]

                converted_image = ImageConversion(
                    original_image=original_image,
                    original_image_name=original_image_name,
                    conversion_status=True,
                    format=format_to
                )

                converted_image_path = f'{original_image.name.split(".")[0]}_{format_to}.{format_extension}'
                conversion.converted_image.save(
                    converted_image_path,
                    converted_image_data, save=True
                )

            except Exception as e:
                print(f"Error during additional conversion: {e}")

    else:
        print("Missing original_image or selected_format in the form data")

    # Retrieve conversion history for displaying on the page
    conversions = ImageConversion.objects.all()
    context = {'conversions': conversions, 'converted_image': converted_image}
    return render(request, 'image_converter/converter.html', context)




from django.http import HttpResponse
from django.shortcuts import get_object_or_404

def download_image(request, image_id):
    conversion = get_object_or_404(ImageConversion, id=image_id)

    if conversion.converted_image:
        file_path = conversion.converted_image.path
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image')
            response['Content-Disposition'] = f'attachment; filename={conversion.original_image_name}.{conversion.format}'
            return response

    return HttpResponse("Image not found", status=404)