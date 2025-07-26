import os
from google.cloud import vision
import google.generativeai as genai

# --- Configuration ---
_is_configured = False

def _ensure_configured():
    """
    Ensures that the necessary API keys are configured before use.
    This is done on-demand to avoid issues with environment variable loading at import time.
    """
    global _is_configured
    if _is_configured:
        return

    # Configure Gemini
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
    genai.configure(api_key=gemini_api_key)

    # Check for Vision API credentials
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set. OCR may fail.")
    
    _is_configured = True

def get_ocr_text(image_path: str) -> str:
    """
    Uses Google Cloud Vision API to extract text from an image.

    Args:
        image_path: The path to the local image file.

    Returns:
        The extracted text as a single string.
    """
    _ensure_configured()
    print(f"Performing OCR on {image_path}...")
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(
            f"{response.error.message}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors"
        )

    if texts:
        return texts[0].description
    else:
        return ""

def analyze_image_with_gemini(image_path: str, ocr_text: str) -> str:
    """
    Analyzes an image and its OCR text using the Gemini model.

    Args:
        image_path: The path to the local image file.
        ocr_text: The text extracted from the image by the Vision API.

    Returns:
        The analysis from the Gemini model.
    """
    _ensure_configured()
    print("Analyzing image with Gemini...")
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Truncate OCR text to avoid exceeding the API limit
    max_ocr_length = 3500
    if len(ocr_text) > max_ocr_length:
        ocr_text = ocr_text[:max_ocr_length] + "\n... [TRUNCATED]"

    # The prompt will combine the visual information from the image
    # with the clean text from the OCR.
    prompt = (
        "Analyse the following image. Here is the text extracted from it, which you can "
        "trust as accurate. Based on both the image and the text, provide a helpful "
        "analysis. What can you see? What might the user be trying to achieve? "
        "Be insightful and proactive.\n\n"
        "IMPORTANT: Your entire analysis must be detailed but concise, and strictly under 1800 characters. "
        "Focus on the most valuable takeaways and use the available space to its full potential.\n\n"
        f"--- OCR TEXT ---\n{ocr_text}\n--- END OCR TEXT ---"
    )
    
    # Generate content using the Gemini model
    image_for_gemini = genai.upload_file(image_path)
    response = model.generate_content([prompt, image_for_gemini])
    
    return response.text


def analyse_image(image_path: str) -> (str, str):
    """
    The main function to orchestrate the full image analysis workflow.

    Args:
        image_path: The path to the local image file.

    Returns:
        A tuple containing:
        - The final analysis string.
        - The raw OCR text string.
    """
    try:
        # Step 1: Extract text using Google Cloud Vision OCR
        ocr_text = get_ocr_text(image_path)

        # Step 2: Analyse the image and text with Gemini
        analysis = analyze_image_with_gemini(image_path, ocr_text)
        
        return analysis, ocr_text

    except Exception as e:
        error_message = f"Sorry, I encountered an error while trying to analyse the image: {e}"
        print(f"An error occurred during image analysis: {e}")
        return error_message, ""

if __name__ == '__main__':
    # This allows for testing the module directly.
    # You would need to create a 'test_image.png' file in the same directory.
    print("Running a direct test of the vision_analyzer module...")
    test_image = "test_image.png"
    if os.path.exists(test_image):
        final_analysis = analyse_image(test_image)
        print("\n--- ANALYSIS RESULT ---")
        print(final_analysis)
        print("-----------------------")
    else:
        print(f"Test image '{test_image}' not found. Please create one to test the module.")