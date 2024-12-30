from cv_screening_model import CVScreener

def main():
    # Initialize the screener
    screener = CVScreener()
    
    # Example job requirements
    job_requirements = """
    Required Skills:
    - Python
    - React
    - Docker
    
    - 3 years of experience
    - Education Level: 2
    """
    
    # Example CVs
    cvs = [
        {
            'candidate_name': 'resume1',
            'file_path': 'resumes/resume1.txt'
        }
    ]
    
    try:
        # Screen CVs
        print("Screening CVs...")
        results = screener.screen_cvs(cvs, job_requirements)
        
        # Print results
        print("\nResults:")
        for rank, (name, score, filepath) in enumerate(results, 1):
            print(f"\nRank {rank}")
            print(f"Candidate: {name}")
            print(f"Score: {score:.2f}")
            print(f"File: {filepath}")
            
    except Exception as e:
        print(f"Error during screening: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 