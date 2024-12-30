from cv_screening_model import CVScreener
import os

def test_cv_screening():
    # Initialize the screener
    screener = CVScreener()
    
    # Test with sample resume
    pdf_path = 'resumes/sample_resume.pdf'
    
    if not os.path.exists(pdf_path):
        print(f"Sample resume not found at {pdf_path}")
        return
        
    print(f"\nTesting PDF extraction for: {pdf_path}")
    
    # Test text extraction
    text = screener.extract_text_from_pdf(pdf_path)
    if text:
        print("\nExtracted text:")
        print("-" * 50)
        print(text)
        print("-" * 50)
        
        # Test skill extraction
        skills = screener.extract_skills(text)
        print("\nExtracted skills:", skills)
        
        # Test scoring
        required_skills = ['Python', 'Java', 'React']
        print("\nTesting scoring with required skills:", required_skills)
        score = screener.calculate_match_score(text, required_skills)
        print(f"Final score: {score:.2f}")
    else:
        print("No text extracted from PDF!")

def test_multiple_formats():
    screener = CVScreener()
    
    # Test files
    test_files = [
        {
            'candidate_name': 'John Doe',
            'file_path': 'resumes/resume1.txt'
        },
        {
            'candidate_name': 'Jane Smith',
            'file_path': 'resumes/resume2.docx'
        },
        {
            'candidate_name': 'Bob Johnson',
            'file_path': 'resumes/resume3.pdf'
        }
    ]
    
    # Test each file
    for file_info in test_files:
        print(f"\nTesting {file_info['file_path']}")
        if os.path.exists(file_info['file_path']):
            text = screener.extract_text(file_info['file_path'])
            print(f"Extracted {len(text)} characters")
            if text:
                skills = screener.extract_skills(text)
                print(f"Found skills: {skills}")
        else:
            print(f"File not found: {file_info['file_path']}")

if __name__ == "__main__":
    # First create a sample resume
    from create_sample_resumes import create_sample_pdf
    create_sample_pdf()
    
    # Then test the CV screening
    test_cv_screening()
    
    test_multiple_formats() 