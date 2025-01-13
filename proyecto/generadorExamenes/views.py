from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PyPDF2 import PdfReader
import requests
import time

@csrf_exempt  # Allows requests without CSRF tokens (use cautiously)
def generate_questions_from_pdf(request):
    print("View 'generate_questions_from_pdf' called")
    
    if request.method == "POST" and request.FILES.get("pdf"):
        pdf_file = request.FILES["pdf"]
        
        try:
            # Read the PDF using PyPDF2
            reader = PdfReader(pdf_file)
            extracted_text = ""

            print("PDF file received and processed")

            for page in reader.pages:
                extracted_text += page.extract_text()

            # Remove null characters from the extracted text
            extracted_text = extracted_text.replace('\0', '')

            # Limit the text length to avoid input size issues
            max_text_length = 5000  # Character limit
            extracted_text = extracted_text[:max_text_length]

            print(f"Extracted text from PDF (first 500 characters): {extracted_text[:500]}")  # Show the first 500 characters of the extracted text

            # Prepare the prompt for the Ollama API
            ollama_url = "http://127.0.0.1:11434/api/chat"
            headers = {"Content-Type": "application/json"}

            # Define the prompt with escaped double quotes for the JSON example
            prompt = f"""
            You are tasked with generating multiple-choice questions from a given text. For each piece of text, you must create one question and provide four possible answers (A, B, C, D). Among these answers, one should be the correct one. Additionally, you need to explain why the correct answer is correct, providing a clear rationale. If relevant, include a quote from the text that supports the answer.

            Format your response as a JSON object, where:
            - "question" is the multiple-choice question.
            - "answers" is an array containing the four answer options (A, B, C, D).
            - "correct_answer" is the letter of the correct answer (A, B, C, or D).
            - "explanation" is a detailed explanation of why the correct answer is right, and why the other options are incorrect.
            - "quote" contains a reference to the part of the text that supports the correct answer.

            Example output format:
            ```json
            {{
                "question": "What is the primary cause of climate change?",
                "answers": {{
                    "A": "Human activity",
                    "B": "Volcanic eruptions",
                    "C": "Solar radiation",
                    "D": "Ocean currents"
                }} ,
                "correct_answer": "A",
                "explanation": "The correct answer is 'Human activity' because scientific research shows that human activities, particularly the burning of fossil fuels, are the main driver of climate change. The other options are less significant contributors.",
                "quote": "According to recent studies, human activity, particularly the burning of fossil fuels, is the primary driver of climate change."
            }}
            ```
            Instructions for handling personal data and sensitive information:
            If the text contains any personal data or sensitive information, such as names, addresses, or private details, you must ignore them and focus solely on the general content of the text. Your responses should never include or refer to personal information.
            Here is the text: {extracted_text}
            """

            # Define messages for the request
            messages = [
                {"role": "system", "content": "This is a new conversation. You will generate multiple-choice questions based on the provided text."},
                {"role": "user", "content": prompt}  # User's prompt with extracted text
            ]

            payload = {
                "model": "llama3.2:1b",  # Replace with the model name available in your Ollama instance
                "messages": messages,
                "stream": False,
                # "format": "json",  # Requesting JSON response
                "options": {
                    "temperature": 0.7  # Optional, adjust as needed
                }
            }

            # Send the request to Ollama API
            response = requests.post(ollama_url, headers=headers, json=payload)

            # Print the raw response for debugging
            print("Raw response from Ollama:", response.text)

            # Check if the response is empty
            if not response.text.strip():
                print("Error: Empty response from Ollama.")
                return JsonResponse({"success": False, "error": "Empty response from Ollama"}, status=500)

            # Try to parse the JSON response
            try:
                result = response.json()
            except ValueError as e:
                print(f"Error parsing JSON response: {e}")
                return JsonResponse({"success": False, "error": "Invalid JSON response"}, status=500)

            # If the response is valid, process it
            if response.status_code == 200:
                try:
                    generated_text = result.get("response", "")
                    if not generated_text:
                        print("Error: No generated text in response.")
                        return JsonResponse({"success": False, "error": "No generated text in response"}, status=500)

                    # Print the generated questions
                    print("Generated questions:", generated_text)

                    # Return the generated questions as JSON
                    return JsonResponse({"success": True, "questions_and_answers": generated_text}, status=200)
                except KeyError as e:
                    print(f"Error extracting generated text: {e}")
                    return JsonResponse({"success": False, "error": "Generated text not found in response"}, status=500)
            else:
                error_message = f"Ollama API error: {response.status_code} - {response.text}"
                print(error_message)
                return JsonResponse({"success": False, "error": error_message}, status=500)

        except Exception as e:
            print(f"Error processing PDF: {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    
    else:
        return JsonResponse({"success": False, "error": "No PDF file provided"}, status=400)
