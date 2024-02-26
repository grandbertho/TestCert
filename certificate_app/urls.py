from django.urls import path
from certificate_app.views import index, generate_pdf

urlpatterns = [
    path('', index, name='index'),
    path('generate_pdf', generate_pdf, name='generate_pdf'),
]
