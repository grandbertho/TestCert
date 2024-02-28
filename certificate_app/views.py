from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import Color
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from datetime import datetime

def generate_certificate(name):
    # Create a response object
    response = HttpResponse(content_type='application/pdf')
    
    # Set the filename and content disposition for download
    response['Content-Disposition'] = f'attachment; filename="{name}_certificate.pdf"'

    # Create a PDF canvas with landscape layout
    p = canvas.Canvas(response, pagesize=landscape(letter))
    pdfmetrics.registerFont(TTFont('Sacrament', 'certificate_app\images\QwitcherGrypen-Bold.ttf'))
    # Add the image
    image_path = "certificate_app/images/certificatehub.png"  # Update with your image path
    p.drawImage(ImageReader(image_path), 0, 0, width=landscape(letter)[0], height=landscape(letter)[1])

    # Set font and font size for the name and date
    p.setFont("Sacrament", 40)

    # Add student name
    name_text = f"{name}"
    name_width = p.stringWidth(name_text)
    name_color = Color(0, 0, 0, alpha=0.85)  # Adjust alpha value as needed (0.5 for 50% opacity)
    p.setFillColor(name_color)
    p.drawString((landscape(letter)[0] - name_width) / 2, 315, name_text)

    # Add current date 
    p.setFont("Times-Italic", 16)
    months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    today = datetime.now()
    day = today.day
    month = months[today.month - 1]  # Adjusted to match with 1-based month index
    year = today.year
    date_text = f"{day} {month} {year}"
    date_width = p.stringWidth(date_text)
    p.drawString((landscape(letter)[0] - date_width) / 2, 220, date_text)

    # Save the PDF
    p.showPage()
    p.save()

    return response

def index(request):
    return render(request, 'index.html')

def generate_pdf(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        return generate_certificate(name)
    else:
        return HttpResponse("Method not allowed")
