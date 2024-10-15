
# Converter Project

This is a Django 5.0-based project for file conversion. The project allows users to convert between different file formats such as images, audio files, documents, PDFs, eBooks, archives, and videos. The project includes various modules for different types of file conversions, allowing users to interact with different conversion endpoints.

## Features

- **Image Converter:** Convert between different image formats (JPG, PNG, BMP, etc.).
- **Audio Converter:** Convert between different audio formats (MP3, WAV, etc.).
- **Document Converter:** Convert documents (DOCX, PDF, PPTX, XLSX, etc.).
- **PDF Converter:** Convert and compress PDFs.
- **Archive Converter:** Compress or decompress archives (ZIP, 7Z, etc.).
- **eBook Converter:** Convert between various eBook formats (EPUB, MOBI, etc.).
- **Video Converter:** Convert between video formats (MP4, AVI, etc.).

## Installation

1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/your-username/converter_project.git
    ```
2. Navigate to the project directory:
    ```bash
    cd converter_project
    ```

3. Create and activate a virtual environment:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

4. Install the project dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Apply migrations to set up the database:
    ```bash
    python manage.py migrate
    ```

6. Run the Django development server:
    ```bash
    python manage.py runserver
    ```

## File Conversions

The project includes the following conversion features:

- Image Conversion: `/image-converter/`
- Audio Conversion: `/audio-converter/`
- Document Conversion: `/document-converter/`
- Archive Conversion: `/archive-converter/`
- PDF Conversion: `/pdf-converter/`
- BMP Conversion: `/bmp-converter/`
- PDF Compression: `/pdf_compressor/`
- Image Compression: `/image_compressor/`
- eBook Conversion: `/ebook-converter/`
- Video Conversion: `/video-converter/`
- Webservice Conversion: `/webservice-converter/`
- Device Conversion: `/device-converter/`

## Requirements

- Python 3.10 or higher
- Django 5.0
- FFmpeg
- OpenCV
- PDF2Docx
- PyMuPDF
- BeautifulSoup4
- Wand

The complete list of requirements is available in the `requirements.txt` and `requirement1.txt` files.

## Project Structure

```
converter_project/
├── converter_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── image_converter/
│   ├── views.py
│   ├── templates/
│   └── ...
├── audio_converter/
│   ├── views.py
│   └── ...
├── ...
├── manage.py
├── requirements.txt
└── requirement1.txt
```

## Usage

1. Upload the file through the relevant endpoint (e.g., `/image-converter/`).
2. The converted file will be processed and available for download on the result page.

## License

This project is licensed under the MIT License.