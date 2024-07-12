Requirements:
  - Python: Version 3.6 or higher
  - PIP
  - Django
  - Djano REST Framework
  - Fitz
  - CV2
  - Tesseract
  - PyTesseract
  - Node.js
  - npm

How to install:
  - Install Python and PIP
  - Go to root "pdf_extract" folder and run commands:
  - "pip install django"
  - "pip install djangorestframework"
  - "pip install PyMuPDF"
  - "pip install opencv-python"
  - "pip install pytesseract"
  - Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki (include croatian language)
  - Include Tesseract in PATH
  - Download Node.js and npm
  - To install all the dependencies run the command: "npm install" from the "frontend" folder.

How to run:
  - Run the command: "python ./manage.py runserver" from the root "pdf_extract" folder.
  - Run the command: "npm run dev" from the "frontend" folder.
