import pytesseract
from PIL import Image
import os

def test_tesseract():
    print("=== Testing Tesseract Setup ===")
    
    # 1. Check Tesseract path
    tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    print(f"\n1. Tesseract Path:")
    print(f"Expected path: {tesseract_path}")
    print(f"Path exists: {os.path.exists(tesseract_path)}")
    
    # 2. Set Tesseract path
    if os.path.exists(tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    # 3. Test version
    try:
        version = pytesseract.get_tesseract_version()
        print(f"\n2. Tesseract Version: {version}")
    except Exception as e:
        print(f"Error getting version: {str(e)}")
    
    # 4. Test simple OCR
    try:
        # Create a simple test image with text
        from PIL import Image, ImageDraw
        
        # Create a new image with white background
        img = Image.new('RGB', (200, 50), color='white')
        d = ImageDraw.Draw(img)
        d.text((10,10), "Test OCR", fill='black')
        
        # Save temporarily
        img.save('test_ocr.png')
        
        # Try OCR
        print("\n3. Testing OCR on simple image:")
        text = pytesseract.image_to_string(img)
        print(f"Extracted text: {text.strip()}")
        
        # Clean up
        os.remove('test_ocr.png')
        
    except Exception as e:
        print(f"Error testing OCR: {str(e)}")

if __name__ == "__main__":
    test_tesseract() 