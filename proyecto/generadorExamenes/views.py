import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PyPDF2 import PdfReader

@csrf_exempt  # Permite solicitudes sin token CSRF (asegúrate de usarlo solo si es necesario)
def generate_questions_from_pdf(request):
    print("Vista 'generate_questions_from_pdf' llamada")
    if request.method == "POST" and request.FILES.get("pdf"):
        pdf_file = request.FILES["pdf"]
        try:
            # Leer el PDF usando PyPDF2
            reader = PdfReader(pdf_file)
            extracted_text = ""

            print("Archivo PDF recibido y procesado")

            for page in reader.pages:
                extracted_text += page.extract_text()

            # Eliminar los caracteres nulos del texto extraído
            extracted_text = extracted_text.replace('\0', '')

            # Limitar la longitud del texto para evitar problemas con la línea de comandos
            max_text_length = 5000  # Límite de caracteres
            extracted_text = extracted_text[:max_text_length]

            print("Texto extraído del PDF:", extracted_text[:500])  # Muestra los primeros 500 caracteres del texto extraído

            # Preparar el texto para la solicitud de Ollama
            command = [
                "ollama", "run",
                "llama3.2:1b",
                extracted_text  # El texto extraído se pasa como un argumento al comando
            ]

            # Usar subprocess para ejecutar el comando
            result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")

            if result.returncode != 0:
                print(f"Error al ejecutar Ollama: {result.stderr}")
                return JsonResponse({"success": False, "error": "Error al ejecutar Ollama: " + result.stderr}, status=500)

            # Imprimir la salida cruda de Ollama
            print("Salida de Ollama:", result.stdout)

            # Devolver el texto generado directamente sin parsear
            return JsonResponse({"success": True, "questions_and_answers": result.stdout}, status=200)

        except Exception as e:
            print(f"Error al procesar el PDF: {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    else:
        return JsonResponse({"success": False, "error": "No se proporcionó un archivo PDF"}, status=400)
