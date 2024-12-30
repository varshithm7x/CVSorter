from pdf2image import convert_from_path
import os

def test_poppler():
    # Test paths
    poppler_path = r'F:\CVSorter\poppler-24.08.0'
    pdf_path = 'uploads/resume1.pdf'
    
    print("Testing Poppler setup:")
    print(f"1. Poppler path exists: {os.path.exists(poppler_path)}")
    
    if os.path.exists(poppler_path):
        print("\nPoppler directory contents:")
        for item in os.listdir(poppler_path):
            print(f"- {item}")
            # If there's a bin directory, show its contents too
            if item == 'bin':
                bin_path = os.path.join(poppler_path, 'bin')
                print("\nContents of bin directory:")
                for bin_item in os.listdir(bin_path):
                    print(f"  - {bin_item}")
    
    print(f"\n2. PDF file exists: {os.path.exists(pdf_path)}")
    
    try:
        print("\n3. Attempting PDF conversion...")
        images = convert_from_path(pdf_path, poppler_path=poppler_path)
        print(f"Success! Converted {len(images)} pages")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_poppler() 