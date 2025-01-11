from django.urls import path
from .views import generate_questions_from_pdf

urlpatterns = [
    path('generate-questions/', generate_questions_from_pdf, name='generate-questions'),
]
