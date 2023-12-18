import zipfile

def is_docx(file_path):
    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            # Check if 'word/document.xml' exists in the archive
            document_xml_exists = 'word/document.xml' in zip_ref.namelist()

            # You can add more checks based on your specific requirements

            return document_xml_exists
    except zipfile.BadZipFile:
        # Handle the case where the file is not a ZIP archive
        return False

# Example usage
file_path = '/home/jabed/Desktop/office/converter_project/media/original_documents/Blood-bank_9zP8KfM.docx'
if is_docx(file_path):
    print(f"{file_path} is a valid DOCX file.")
else:
    print(f"{file_path} is not a valid DOCX file.")
