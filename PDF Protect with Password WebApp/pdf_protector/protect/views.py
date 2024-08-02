import os
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from PyPDF2 import PdfReader, PdfWriter

def home(request):
    if request.method == 'POST' and request.FILES.get('pdf'):
        pdf = request.FILES['pdf']
        password = request.POST['password']
        fs = FileSystemStorage()
        filename = fs.save(pdf.name, pdf)
        file_url = fs.url(filename)

        # Protect the PDF with a password
        protected_pdf_path = protect_pdf_with_password(fs.path(filename), password)

        # Serve the protected PDF for download
        return redirect('protected_pdf', path=protected_pdf_path)

    return render(request, 'home.html')

def protect_pdf_with_password(pdf_path, password):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)
    protected_pdf_path = pdf_path.replace('.pdf', '_protected.pdf')
    with open(protected_pdf_path, 'wb') as f:
        writer.write(f)

    return protected_pdf_path

def protected_pdf(request, path):
    return render(request, 'protected_pdf.html', {'file_path': path})
