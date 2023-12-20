import os
import tempfile
from django.shortcuts import redirect, render
from pydub import AudioSegment
from django.contrib.sites.shortcuts import get_current_site


def audio_converter(request):
    if request.method == 'POST':
        original_audio = request.FILES['original_audio']
        format_to = request.POST['audio_format']

        if original_audio and format_to:
            try:
                # Create a temporary folder for conversion
                temp_folder_path = tempfile.mkdtemp(prefix='temp_audio_conversion_', dir='media')

                # Save the original file in the temporary folder with a unique name
                original_file_name = f"original.{format_to}"
                original_file_path = os.path.join(temp_folder_path, original_file_name)

                with open(original_file_path, 'wb+') as destination:
                    for chunk in original_audio.chunks():
                        destination.write(chunk)

                # Load the original audio file using pydub
                audio = AudioSegment.from_file(original_file_path)

                # Convert and save the audio to the desired format
                converted_file_name = f"converted.{format_to}"
                converted_audio_path = os.path.join('media', converted_file_name)
                # audio.export(converted_audio_path, format=format_to.upper())  # Ensure the format is uppercase
                
                export_args = {}
                if format_to.lower() == 'aac':
                    export_args['format'] = 'mp3'
                    export_args['codec'] = 'aac'
                    export_args['parameters'] = ['-strict', 'experimental']

                audio.export(converted_audio_path, **export_args)

                # Clean up the temporary folder
                os.remove(original_file_path)
                os.rmdir(temp_folder_path)

                # Generate the download link
                current_site = get_current_site(request)
                download_link = f'{request.scheme}://{current_site.domain}/media/{converted_file_name}'

                request.session['download_link'] = download_link

                # Render the template with the converted file link
                return redirect('audio_result_page')

            except Exception as e:
                print(f"Error during audio conversion: {e}")

    else:
        print("Missing original_audio or audio_format in the form data")

    return render(request, 'audio_converter/converter.html')

def audio_result_page(request):
    download_link = request.session.pop('download_link', None)

    return render(request, 'audio_converter/result_page.html', {'download_link': download_link})
