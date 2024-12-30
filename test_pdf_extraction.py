from cv_screening_model import CVScreener
import os

def test_pdf_extraction():
    screener = CVScreener()
    pdf_path = 'uploads/resume1.pdf'  # Adjust path as needed
    
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return
    
    print(f"Testing PDF extraction for: {pdf_path}")
    print("File size:", os.path.getsize(pdf_path), "bytes")
    
    text = screener.extract_text_from_pdf(pdf_path)
    
    if text:
        print("\nExtraction successful!")
        print("Text length:", len(text))
        print("\nFirst 500 characters:")
        print("-" * 50)
        print(text[:500])
        print("-" * 50)
        
        # Test skill extraction
        skills = screener.extract_skills(text)
        print("\nFound skills:", skills)
    else:
        print("No text extracted from PDF!")

if __name__ == "__main__":
    test_pdf_extraction() 