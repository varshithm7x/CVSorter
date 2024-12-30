import os
import sys
from pdf2image import convert_from_path
import pytesseract

def test_environment():
    print("=== Testing Environment Setup ===")
    
    # 1. Check Python version
    print(f"\n1. Python Version: {sys.version}")
    
    # 2. Check Poppler
    poppler_base = r'F:\CVSorter\poppler-24.08.0'
    poppler_bin = os.path.join(poppler_base, 'Library', 'bin')
    print(f"\n2. Poppler Setup:")
    print(f"Base path exists: {os.path.exists(poppler_base)}")
    print(f"Bin path exists: {os.path.exists(poppler_bin)}")
    
    if os.path.exists(poppler_bin):
        print("\nPoppler bin contents:")
        for item in os.listdir(poppler_bin):
            print(f"- {item}")
    
    # 3. Check Tesseract
    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    print(f"\n3. Tesseract Setup:")
    print(f"Path exists: {os.path.exists(tesseract_path)}")
    
    # 4. Test PDF conversion
    try:
        pdf_path = 'uploads/resume1.pdf'
        print(f"\n4. Testing PDF conversion:")
        print(f"PDF exists: {os.path.exists(pdf_path)}")
        if os.path.exists(pdf_path):
            images = convert_from_path(
                pdf_path,
                poppler_path=poppler_bin
            )
            print(f"Successfully converted {len(images)} pages")
            
            # Test OCR
            print("\n5. Testing OCR:")
            text = pytesseract.image_to_string(images[0])
            print(f"Extracted {len(text)} characters from first page")
            print("First 100 characters:", text[:100])
    except Exception as e:
        print(f"Error during testing: {str(e)}")

if __name__ == "__main__":
    test_environment() 