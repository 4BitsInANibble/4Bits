from PIL import Image
import pytesseract


# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows Only: Update this path to where Tesseract is installed

# Function to perform OCR on an image file and return the text
def ocr_image(image_path):
    # Load the image from the specified path
    image = Image.open(image_path)
    
    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(image)
    

    # Print or save the extracted text
    print(text)
    # Optionally, save the text to a file
    with open('extracted_text.txt', 'w', encoding='utf-8') as file:
        file.write(text)

    return text