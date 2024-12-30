from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os

def create_sample_pdf():
    # Create resumes directory if it doesn't exist
    if not os.path.exists('resumes'):
        os.makedirs('resumes')

    # Create a sample PDF
    pdf_path = 'resumes/sample_resume.pdf'
    c = canvas.Canvas(pdf_path, pagesize=letter)
    
    # Add text content
    c.drawString(72, 750, "John Doe")
    c.drawString(72, 730, "Software Engineer")
    
    # Skills section
    c.drawString(72, 700, "Skills:")
    c.drawString(72, 680, "Python, Java, JavaScript")
    c.drawString(72, 660, "React, Node.js, Docker")
    
    # Experience section
    c.drawString(72, 620, "Experience:")
    c.drawString(72, 600, "Senior Developer - Tech Corp (2018-Present)")
    c.drawString(72, 580, "- Led development team of 5 engineers")
    c.drawString(72, 560, "- Implemented CI/CD pipeline using Jenkins")
    
    # Education section
    c.drawString(72, 520, "Education:")
    c.drawString(72, 500, "Master's in Computer Science")
    
    c.save()
    print(f"Created sample resume at {pdf_path}")

if __name__ == "__main__":
    create_sample_pdf() 