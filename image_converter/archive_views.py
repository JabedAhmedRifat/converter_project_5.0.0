import os
import tempfile
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template.loader import render_to_string
from shutil import make_archive, copy2
import py7zr
import tarfile




def archive_converter(request):
    if request.method == 'POST':
        original_folder = request.FILES['original_folder']
        format_to = request.POST['archive_format']

        if original_folder and format_to:
            try:
                # Create a temporary folder for conversion
                temp_folder_path = tempfile.mkdtemp(prefix='temp_conversion_', dir='media')

                # Save the original file in the temporary folder with a unique name
                original_file_name = f"original_{original_folder.name}"
                original_file_path = os.path.join(temp_folder_path, original_file_name)

                with open(original_file_path, 'wb+') as destination:
                    for chunk in original_folder.chunks():
                        destination.write(chunk)

                # Create the archive based on the selected format
                converted_archive_name = f"converted.{format_to}"
                converted_archive_path = os.path.join('media', f"converted.{format_to}")
                
                if format_to == 'zip':
                    make_archive(converted_archive_path, 'zip', temp_folder_path)
                    
                elif format_to == '7z':
                    with py7zr.SevenZipFile(converted_archive_path, 'w') as archive:
                        archive.writeall(temp_folder_path)
                        
                        
                        
                elif format_to == 'tar':
                    # Create the tar archive without compression
                    tar_archive_path = f"{converted_archive_path[:-4]}.tar"  # Remove the compression extension
                    with tarfile.open(tar_archive_path, 'w') as tar:
                        tar.add(temp_folder_path, arcname=original_file_name)
                    # shutil.move(tar_archive_path, converted_archive_path)
                    
                    
                elif format_to == 'tar.bz2':
                # Create the tar.bz2 archive
                    with tarfile.open(converted_archive_path, 'w:bz2') as tar:
                        tar.add(temp_folder_path, arcname=original_file_name)
                        
                        
                elif format_to == 'tar.gz':
                    # Create the tar.gz archive
                    with tarfile.open(converted_archive_path, 'w:gz') as tar:
                        tar.add(temp_folder_path, arcname=original_file_name)
                        
                # elif format_to in ['tar', 'tar.bz2', 'tar.gz']:
                #     with tarfile.open(converted_archive_path, f'w:{format_to}') as tar:
                #         tar.add(temp_folder_path, arcname=original_file_name)



                # Clean up the temporary folder
                for file_name in os.listdir(temp_folder_path):
                    file_path = os.path.join(temp_folder_path, file_name)
                    os.remove(file_path)
                os.rmdir(temp_folder_path)
                
                
                # Generate the download link using Django's reverse function
                download_link = request.build_absolute_uri(f'/media/{converted_archive_name}')
                
                request.session['download_link'] = download_link

                # Render the template with the converted file link
                return redirect('archive_result_page')

                


            except Exception as e:
                print(f"Error during archive conversion: {e}")

    else:
        print("Missing original_folder or selected_format in the form data")

    return render(request, 'archive_converter/converter.html')





def archive_result_page(request):
    download_link = request.session.pop('download_link', None)

    return render(request, 'archive_converter/result_page.html', {'download_link': download_link})







































# import os
# import magic
# from django.shortcuts import render
# from django.http import HttpResponse
# from .models import ArchiveConversion
# from django.shortcuts import get_object_or_404
# from shutil import make_archive, copy2
# import py7zr
# import tarfile


# def archive_converter(request):
#     if request.method == 'POST':
#         original_folder = request.FILES['original_folder']
#         format_to = request.POST['archive_format']

#         if original_folder and format_to:
#             conversion = ArchiveConversion(original_folder=original_folder)
#             conversion.save()

#             # Get the path for the uploaded folder
#             original_folder_path = os.path.join('media', str(conversion.original_folder))

#             try:
#                 # Conversion logic for different archive formats
#                 if format_to == 'zip':
#                     # Create a zip archive
#                     zip_path = os.path.join('media', f"{conversion.original_folder_name}.zip")
#                     make_archive(zip_path, 'zip', original_folder_path)

#                 elif format_to == '7z':
#                     # Create a 7z archive
#                     seven_zip_path = os.path.join('media', f"{conversion.original_folder_name}.7z")
#                     with py7zr.SevenZipFile(seven_zip_path, 'w') as archive:
#                         archive.writeall(original_folder_path)

#                 elif format_to == 'tar':
#                     # Create a tar archive using the tarfile library
#                     tar_path = os.path.join('media', f"{conversion.original_folder_name}.tar")
#                     with tarfile.open(tar_path, 'w') as tar:
#                         tar.add(original_folder_path, arcname=os.path.basename(original_folder_path))


#                 elif format_to == 'tar.bz2':
#                     # Create a tar.bz2 archive using the tarfile library
#                     tar_bz2_path = os.path.join('media', f"{conversion.original_folder_name}.tar.bz2")
#                     with tarfile.open(tar_bz2_path, 'w:bz2') as tar:
#                         tar.add(original_folder_path, arcname=os.path.basename(original_folder_path))

                
#                 elif format_to == 'tar.gz':
#                     # Create a tar.gz archive using the tarfile library
#                     tar_gz_path = os.path.join('media', f"{conversion.original_folder_name}.tar.gz")
#                     with tarfile.open(tar_gz_path, 'w:gz') as tar:
#                         tar.add(original_folder_path, arcname=os.path.basename(original_folder_path))



#                 conversion.conversion_status = True
#                 conversion.format = format_to

#                 # Copy the converted file to the appropriate location
#                 converted_archive_path = f'{conversion.original_folder_name}.{format_to}'
#                 copy2(os.path.join('media', converted_archive_path), os.path.join('media', 'converted_archives'))

#                 # Save the converted file path in the database
#                 conversion.converted_archive.name = os.path.join(converted_archive_path)
#                 conversion.save()

#             except Exception as e:
#                 print(f"Error during archive conversion: {e}")

#     else:
#         print("Missing original_folder or selected_format in the form data")

#     # Retrieve conversion history for displaying on the page
#     conversions = ArchiveConversion.objects.all()
#     context = {'conversions': conversions}
#     return render(request, 'archive_converter/converter.html', context)


# def download_archive(request, archive_id):
#     conversion = get_object_or_404(ArchiveConversion, id=archive_id)

#     if conversion.converted_archive:
#         file_path = conversion.converted_archive.path
#         with open(file_path, 'rb') as f:
#             response = HttpResponse(f.read(), content_type='application/octet-stream')
#             response['Content-Disposition'] = f'attachment; filename={conversion.original_folder_name}.{conversion.format}'
#             return response

#     return HttpResponse("Document not found", status=404)
