from pdf2image import convert_from_path
import os

def test_poppler_setup():
    print("Current working directory:", os.getcwd())
    
    # List contents of current directory
    print("\nContents of current directory:")
    for item in os.listdir('.'):
        print(item)
    
    # Check poppler installation
    poppler_path = r'F:\CVSorter\poppler-24.08.0\Library\bin'
    print(f"\nChecking poppler path: {poppler_path}")
    print(f"Poppler exists: {os.path.exists(poppler_path)}")
    
    if os.path.exists(poppler_path):
        print("\nContents of poppler bin directory:")
        for item in os.listdir(poppler_path):
            print(item)
    
    # Test PDF conversion
    pdf_path = 'uploads/resume1.pdf'
    print(f"\nTesting PDF conversion: {pdf_path}")
    print(f"PDF exists: {os.path.exists(pdf_path)}")
    
    try:
        images = convert_from_path(pdf_path, poppler_path=poppler_path)
        print(f"Successfully converted PDF to {len(images)} images")
    except Exception as e:
        print(f"Error converting PDF: {str(e)}")

if __name__ == "__main__":
    test_poppler_setup() 