from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os

def test_pdf_ocr():
    print("=== Testing PDF to OCR Pipeline ===")
    
    # Set Tesseract path explicitly with the correct path
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    
    # Test configuration
    poppler_path = r'F:\CVSorter\poppler-24.08.0\Library\bin'
    pdf_path = 'resumes/sample_resume.pdf'
    
    print("\n1. Checking paths:")
    print(f"Poppler path exists: {os.path.exists(poppler_path)}")
    print(f"PDF file exists: {os.path.exists(pdf_path)}")
    print(f"Tesseract exists: {os.path.exists(pytesseract.pytesseract.tesseract_cmd)}")
    
    try:
        print("\n2. Converting PDF to images...")
        images = convert_from_path(pdf_path, poppler_path=poppler_path)
        print(f"Successfully converted {len(images)} pages")
        
        print("\n3. Testing OCR on first page...")
        # Save first page temporarily
        temp_image_path = 'temp_test_page.png'
        images[0].save(temp_image_path)
        
        # Try OCR with explicit configuration
        text = pytesseract.image_to_string(
            Image.open(temp_image_path),
            lang='eng',
            config='--psm 1'
        )
        
        print(f"Extracted {len(text)} characters")
        print("\nFirst 200 characters of extracted text:")
        print("-" * 50)
        print(text[:200])
        print("-" * 50)
        
        # Clean up
        os.remove(temp_image_path)
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        print(f"Current directory: {os.getcwd()}")

if __name__ == "__main__":
    test_pdf_ocr() 