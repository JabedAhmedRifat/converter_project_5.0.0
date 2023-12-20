import os
import tempfile
from django.shortcuts import render, redirect
from moviepy.editor import VideoFileClip

def video_converter(request):
    if request.method == 'POST':
        original_video = request.FILES['original_video']
        format_to = request.POST['video_format']

        if original_video and format_to:
            try:
                # Create a temporary folder for conversion
                temp_folder_path = tempfile.mkdtemp(prefix='temp_conversion_', dir='media')

                # Save the original file in the temporary folder with a unique name
                original_file_name = f"original.{format_to}"
                original_file_path = os.path.join(temp_folder_path, original_file_name)

                with open(original_file_path, 'wb+') as destination:
                    for chunk in original_video.chunks():
                        destination.write(chunk)

                # Load the original video clip
                clip = VideoFileClip(original_file_path)

                # Define the output file name with the new format
                converted_file_name = f"converted.{format_to}"
                converted_video_path = os.path.join('media', converted_file_name)

                # Specify the appropriate codec parameters based on the format
                if format_to in ['webm']:
                    clip.write_videofile(converted_video_path, codec='libvpx', audio_codec='libvorbis')
                elif format_to in ['mpg']:
                    clip.write_videofile(converted_video_path, codec='libx264', audio_codec='mp2')
                elif format_to in ['ogv']:
                    clip.write_videofile(converted_video_path, codec='libtheora', audio_codec='libvorbis')
                else:
                    # For other formats, use the original parameters
                    clip.write_videofile(converted_video_path, codec='libx264', audio_codec='aac')

                # Clean up the temporary folder
                os.remove(original_file_path)
                os.rmdir(temp_folder_path)

                # Generate the download link
                download_link = f'/media/{converted_file_name}'

                request.session['download_link'] = download_link

                # Render the template with the converted file link
                return redirect('video_result_page')

            except Exception as e:
                print(f"Error during video conversion: {e}")

    else:
        print("Missing original_video or video_format in the form data")

    return render(request, 'video_converter/converter.html')




def video_result_page(request):
    download_link = request.session.pop('download_link', None)

    return render(request, 'video_converter/result_page.html', {'download_link': download_link})
