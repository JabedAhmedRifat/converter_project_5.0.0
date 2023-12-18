import os
import io
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from pydub import AudioSegment
from pydub.playback import play
from pydub.generators import Sine
from .models import AudioConversion
import subprocess

import ffmpeg

from django.http import JsonResponse

def audio_converter(request):
    converted_audio = None
    format_extension = None

    if request.method == 'POST':
        original_audio = request.FILES['original_audio']
        format_to = request.POST['audio_format']

        # Save the original audio details to the database
        conversion = AudioConversion(original_audio=original_audio, original_audio_name=original_audio.name)
        conversion.save()

        # Get the path for the uploaded audio
        original_audio_path = os.path.join('media', str(conversion.original_audio))
        original_audio_format = original_audio_path.split('.')[-1]

        # Conversion logic for different formats
        with open(original_audio_path, 'rb') as audio_file:
            original_audio_data = io.BytesIO(audio_file.read())
            original_audio_pydub = AudioSegment.from_file(original_audio_data)

            if original_audio_format == 'mp3' and format_to == 'wav':
                input_file = original_audio_path
                output_file = format_to + '.wav'  # Specify the output format
                ffmpeg.input(input_file).output(output_file, ar=44100, ac=2).run()
                format_extension = 'wav'




            elif original_audio_format == 'mp3' and format_to == 'mp3':
                original_audio_pydub.export(format_to, format='mp3')
                format_extension = 'mp3'


            elif original_audio_format == 'mp3' and format_to == 'ogg':
                original_audio_pydub.export(format_to, format='ogg')
                format_extension = 'ogg'

            elif original_audio_format == 'mp3' and format_to == 'flac':
                original_audio_pydub.export(format_to, format='flac')
                format_extension = 'flac'

            elif original_audio_format == 'mp3' and format_to == 'aac':
                original_audio_pydub.export(format_to, format='aac')
                format_extension = 'aac'

            elif original_audio_format == 'mp3' and format_to == 'm4a':
                original_audio_pydub.export(format_to, format='m4a')
                format_extension = 'm4a'

            elif original_audio_format == 'mp3' and format_to == 'opus':
                original_audio_pydub.export(format_to, format='opus')
                format_extension = 'opus'

            elif original_audio_format == 'mp3' and format_to == 'wma':
                # Using subprocess for mp3 to wma conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'wma'

            # WAV to all format options
            elif original_audio_format == 'wav' and format_to == 'mp3':
                original_audio_pydub.export(format_to, format='mp3')
                format_extension = 'mp3'

            elif original_audio_format == 'wav' and format_to == 'ogg':
                original_audio_pydub.export(format_to, format='ogg')
                format_extension = 'ogg'

            elif original_audio_format == 'wav' and format_to == 'flac':
                original_audio_pydub.export(format_to, format='flac')
                format_extension = 'flac'

            elif original_audio_format == 'wav' and format_to == 'aac':
                original_audio_pydub.export(format_to, format='aac')
                format_extension = 'aac'

            elif original_audio_format == 'wav' and format_to == 'm4a':
                original_audio_pydub.export(format_to, format='m4a')
                format_extension = 'm4a'

            elif original_audio_format == 'wav' and format_to == 'opus':
                original_audio_pydub.export(format_to, format='opus')
                format_extension = 'opus'

            elif original_audio_format == 'wav' and format_to == 'wma':
                # Using subprocess for wav to wma conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'wma'

             # OGG to all format options
            elif original_audio_format == 'ogg' and format_to == 'mp3':
                # Using subprocess for ogg to mp3 conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'mp3'

            elif original_audio_format == 'ogg' and format_to == 'wav':
                # Using subprocess for ogg to wav conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'wav'

            elif original_audio_format == 'ogg' and format_to == 'flac':
                # Using subprocess for ogg to flac conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'flac'

            elif original_audio_format == 'ogg' and format_to == 'aac':
                # Using subprocess for ogg to aac conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'aac'

            elif original_audio_format == 'ogg' and format_to == 'm4a':
                # Using subprocess for ogg to m4a conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'm4a'

            elif original_audio_format == 'ogg' and format_to == 'opus':
                # Using subprocess for ogg to opus conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'opus'

            elif original_audio_format == 'ogg' and format_to == 'wma':
                # Using subprocess for ogg to wma conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'wma'

            elif original_audio_format == 'flac' and format_to == 'mp3':
                # Using subprocess for flac to mp3 conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'mp3'

            elif original_audio_format == 'flac' and format_to == 'wav':
                # Using subprocess for flac to wav conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'wav'

            elif original_audio_format == 'flac' and format_to == 'ogg':
                # Using subprocess for flac to ogg conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'ogg'

            elif original_audio_format == 'flac' and format_to == 'aac':
                # Using subprocess for flac to aac conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'aac'

            elif original_audio_format == 'flac' and format_to == 'm4a':
                # Using subprocess for flac to m4a conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'm4a'

            elif original_audio_format == 'flac' and format_to == 'opus':
                # Using subprocess for flac to opus conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'opus'

            elif original_audio_format == 'flac' and format_to == 'wma':
                # Using subprocess for flac to wma conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'wma'


            elif original_audio_format == 'aac' and format_to == 'mp3':
                original_audio_pydub.export(format_to, format='mp3')
                format_extension = 'mp3'

            elif original_audio_format == 'aac' and format_to == 'wav':
                original_audio_pydub.export(format_to, format='wav')
                format_extension = 'wav'

            elif original_audio_format == 'aac' and format_to == 'ogg':
                original_audio_pydub.export(format_to, format='ogg')
                format_extension = 'ogg'

            elif original_audio_format == 'aac' and format_to == 'flac':
                original_audio_pydub.export(format_to, format='flac')
                format_extension = 'flac'

            elif original_audio_format == 'aac' and format_to == 'm4a':
                original_audio_pydub.export(format_to, format='m4a')
                format_extension = 'm4a'

            elif original_audio_format == 'aac' and format_to == 'opus':
                original_audio_pydub.export(format_to, format='opus')
                format_extension = 'opus'

            elif original_audio_format == 'aac' and format_to == 'wma':
                # Using subprocess for aac to wma conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'wma'



            # M4A to all format options
            elif original_audio_format == 'm4a' and format_to == 'mp3':
                original_audio_pydub.export(format_to, format='mp3')
                format_extension = 'mp3'

            elif original_audio_format == 'm4a' and format_to == 'wav':
                original_audio_pydub.export(format_to, format='wav')
                format_extension = 'wav'

            elif original_audio_format == 'm4a' and format_to == 'ogg':
                original_audio_pydub.export(format_to, format='ogg')
                format_extension = 'ogg'

            elif original_audio_format == 'm4a' and format_to == 'flac':
                original_audio_pydub.export(format_to, format='flac')
                format_extension = 'flac'

            elif original_audio_format == 'm4a' and format_to == 'aac':
                original_audio_pydub.export(format_to, format='aac')
                format_extension = 'aac'

            elif original_audio_format == 'm4a' and format_to == 'opus':
                original_audio_pydub.export(format_to, format='opus')
                format_extension = 'opus'

            elif original_audio_format == 'm4a' and format_to == 'wma':
                # Using subprocess for m4a to wma conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'wma'


            # OPUS to all format options
            elif original_audio_format == 'opus' and format_to == 'mp3':
                # Using subprocess for opus to mp3 conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'mp3'

            elif original_audio_format == 'opus' and format_to == 'wav':
                # Using subprocess for opus to wav conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'wav'

            elif original_audio_format == 'opus' and format_to == 'ogg':
                # Using subprocess for opus to ogg conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'ogg'

            elif original_audio_format == 'opus' and format_to == 'flac':
                # Using subprocess for opus to flac conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'flac'

            elif original_audio_format == 'opus' and format_to == 'aac':
                # Using subprocess for opus to aac conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'aac'

            elif original_audio_format == 'opus' and format_to == 'm4a':
                # Using subprocess for opus to m4a conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'm4a'

            elif original_audio_format == 'opus' and format_to == 'wma':
                # Using subprocess for opus to wma conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'wma'


            # WMA to all format options
            elif original_audio_format == 'wma' and format_to == 'mp3':
                # Using subprocess for wma to mp3 conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'mp3'

            elif original_audio_format == 'wma' and format_to == 'wav':
                # Using subprocess for wma to wav conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'wav'

            elif original_audio_format == 'wma' and format_to == 'ogg':
                # Using subprocess for wma to ogg conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'ogg'

            elif original_audio_format == 'wma' and format_to == 'flac':
                # Using subprocess for wma to flac conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'flac'

            elif original_audio_format == 'wma' and format_to == 'aac':
                # Using subprocess for wma to aac conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'aac'

            elif original_audio_format == 'wma' and format_to == 'm4a':
                # Using subprocess for wma to m4a conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'm4a'

            elif original_audio_format == 'wma' and format_to == 'opus':
                # Using subprocess for wma to opus conversion
                subprocess.run(["ffmpeg", "-i", original_audio_path, format_to])
                format_extension = 'opus'

# Add more conversion options as needed



            # Add more conversion options as needed

            # Update the conversion model with the format and status
            conversion.conversion_status = True
            conversion.format = format_to
            conversion.save()

            try:
                # Create a new AudioConversion instance for the converted audio
                converted_audio = AudioConversion(
                    original_audio=conversion.original_audio,  # Use the original audio from the conversion
                    original_audio_name=os.path.splitext(original_audio.name)[0],
                    conversion_status=True,
                    format=format_to
                )

                # Save the converted audio file to the model instance
                converted_audio_path = f'{original_audio.name.split(".")[0]}_{format_to}.{format_extension}'
                converted_audio.converted_audio.save(
                    converted_audio_path,
                    content=io.BytesIO(original_audio_pydub.raw_data),
                    save=True
                )

               


            except Exception as e:
                print(f"Error during additional conversion: {e}")
                return HttpResponse("Internal Server Error", status=500)

    else:
        print("Missing original_audio or selected_format in the form data")

    # Retrieve conversion history for displaying on the page
    conversions = AudioConversion.objects.all()
    context = {'conversions': conversions, 'converted_audio': converted_audio}
    return render(request, 'audio_converter/converter.html', context)



from django.shortcuts import get_object_or_404
from django.http import FileResponse
import mimetypes

def download_audio(request, audio_id):
    conversion = get_object_or_404(AudioConversion, id=audio_id)

    if conversion.converted_audio:
        file_path = conversion.converted_audio.path

        # Use FileResponse to serve the file
        response = FileResponse(open(file_path, 'rb'))

        # Set content type based on file extension
        content_type, encoding = mimetypes.guess_type(file_path)
        response['Content-Type'] = content_type

        # Force download
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        return response

    return HttpResponse("Audio not found", status=404)