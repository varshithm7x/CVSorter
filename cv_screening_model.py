import spacy
import re
from pdf2image import convert_from_path
import pytesseract
import platform
import os
from PIL import Image
from datetime import datetime

class CVScreener:
    def __init__(self):
        # Load spaCy model
        self.nlp = spacy.load('en_core_web_sm')
        
        # Use system-installed Tesseract and Poppler
        if platform.system() == 'Windows':
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            # Update path to match your actual Poppler location
            self.poppler_path = r'F:\CVSorter\poppler-24.08.0\Library\bin'
        else:
            # On Linux/deployment, use system installed versions
            self.poppler_path = None  # System default
        
        # Initialize custom_skills
        self.custom_skills = []
        
        # Define language patterns as class attribute
        self.lang_patterns = [
            # Ruby patterns - must be specific to avoid matching single 'R'
            (r'\bruby\b|\bruby\s*on\s*rails\b|\bruby/rails\b|\bruby-on-rails\b|\bror\b|\brails\b|ruby developer|rails developer', 'Ruby'),
            # R pattern - must be standalone 'R' with word boundaries
            (r'\br\b(?!\s*studio)|\br\s+programming\b|\br\s+language\b', 'R'),
            # Other languages...
            (r'\b(java|core\s*java|java\s*se|java\s*ee)\b', 'Java'),
            (r'\b(javascript|js|node\.?js|nodejs)\b', 'JavaScript'),
            (r'\b(python|py|python3)\b', 'Python'),
            (r'\b(sql|mysql|postgresql|oracle|sqlite|pl\/sql)\b', 'SQL'),
            (r'\b(html|html5)\b', 'HTML'),
            (r'\b(css|css3|scss|sass)\b', 'CSS'),
            (r'\bc\+\+\b', 'C++'),
            (r'\b(c#|csharp|\.net)\b', 'C#'),
            (r'\b(react|reactjs|react\.js)\b', 'React'),
            (r'\b(angular|angularjs)\b', 'Angular'),
            (r'\b(node|nodejs|node\.js)\b', 'Node.js'),
            (r'\b(git|github|gitlab)\b', 'Git'),
            (r'\b(docker|container)\b', 'Docker'),
            (r'\b(aws|amazon\s*web\s*services)\b', 'AWS'),
            (r'\b(azure|microsoft\s*azure)\b', 'Azure')
        ]

    def extract_text_from_pdf(self, file_path):
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return ""
            
            # Convert PDF to images
            if platform.system() == 'Windows':
                if not os.path.exists(self.poppler_path):
                    return ""
                images = convert_from_path(
                    file_path,
                    poppler_path=self.poppler_path,
                    dpi=300
                )
            else:
                images = convert_from_path(file_path, dpi=300)
            
            # Process each page
            text = ""
            for i, image in enumerate(images):
                try:
                    # Preprocess image
                    img = image.convert('L')
                    
                    # Save image temporarily
                    temp_image_path = f'temp_page_{i}.png'
                    img.save(temp_image_path, dpi=(300, 300))
                    
                    # Try OCR configurations
                    configs = [
                        '--psm 1',  # Automatic page segmentation with OSD
                        '--psm 3',  # Fully automatic page segmentation
                        '--psm 6'   # Assume a uniform block of text
                    ]
                    
                    page_text = ""
                    for config in configs:
                        current_text = pytesseract.image_to_string(
                            Image.open(temp_image_path),
                            lang='eng',
                            config=f'{config} --oem 3'
                        )
                        
                        if len(current_text) > len(page_text):
                            page_text = current_text
                    
                    text += page_text + "\n"
                    
                    # Clean up
                    os.remove(temp_image_path)
                    
                except Exception as e:
                    continue
            
            return text.strip()
            
        except Exception as e:
            return ""

    def extract_skills(self, text):
        found_skills = []
        # Clean the text first
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        
        # Find all skills using predefined patterns
        for pattern, skill_name in self.lang_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                found_skills.append(skill_name)
        
        # Check for custom skills with more flexible matching
        for skill in self.custom_skills:
            # Create variations of the skill
            skill_variations = [
                skill.lower(),  # exact match
                skill.lower().replace(' ', ''),  # no spaces
                skill.lower().replace('system', 'systems'),  # system/systems variation
                skill.lower().replace('systems', 'system'),  # systems/system variation
                re.sub(r'\s+', '.*', skill.lower())  # flexible word spacing
            ]
            
            # Try each variation
            for variation in skill_variations:
                # Create pattern that matches the variation with flexible boundaries
                skill_pattern = r'\b' + re.escape(variation).replace('\\ ', r'\s*') + r'\b'
                if re.search(skill_pattern, text, re.IGNORECASE):
                    found_skills.append(skill)  # Add the original skill name
                    break  # Break once we find a match
                
                # Try fuzzy matching for longer skill names
                if len(skill.split()) > 1:  # Only for multi-word skills
                    words = skill.lower().split()
                    if all(re.search(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE) 
                          for word in words):
                        found_skills.append(skill)
                        break
        
        # Remove duplicates while preserving order
        unique_skills = []
        seen = set()
        for skill in found_skills:
            if skill.lower() not in seen:
                seen.add(skill.lower())
                unique_skills.append(skill)
        
        return unique_skills

    def extract_experience(self, text):
        """Extract years of experience from CV text"""
        try:
            # Normalize text
            text = text.lower()
            text = re.sub(r'\s+', ' ', text)
            
            # Simple experience patterns
            patterns = [
                # Basic year patterns
                r'(\d+)\s*(?:\+\s*)?year',
                r'(\d+)\s*(?:\+\s*)?yr',
                r'(\d+)\s*(?:\+\s*)?yrs',
                
                # Experience with years
                r'experience:?\s*(\d+)',
                r'(\d+)\s*years?\s*experience',
                r'(\d+)\s*years?\s*of\s*experience',
                
                # Work experience
                r'worked\s*(?:for)?\s*(\d+)\s*years?',
                r'working\s*(?:for)?\s*(\d+)\s*years?',
                
                # Professional experience
                r'professional\s*experience:?\s*(\d+)',
                r'industry\s*experience:?\s*(\d+)',
                
                # Total experience
                r'total\s*experience:?\s*(\d+)',
                r'total\s*(?:of)?\s*(\d+)\s*years?'
            ]
            
            # Try each pattern
            for pattern in patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    try:
                        years = int(match.group(1))
                        if 0 < years <= 50:  # Sanity check
                            return years
                    except ValueError:
                        continue
            
            # If no explicit years found, try to find date ranges
            date_pattern = r'((?:19|20)\d{2})\s*(?:-|to|–|until)\s*((?:present|current|now|(?:19|20)\d{2}))'
            matches = re.finditer(date_pattern, text)
            
            for match in matches:
                try:
                    start_year = int(match.group(1))
                    end_text = match.group(2)
                    
                    if end_text.lower() in ['present', 'current', 'now']:
                        end_year = datetime.now().year
                    else:
                        end_year = int(end_text)
                    
                    years = end_year - start_year
                    if 0 < years <= 50:
                        return years
                except ValueError:
                    continue
            
            return 0
            
        except Exception as e:
            print(f"Error extracting experience: {e}")
            return 0

    def calculate_match_score(self, cv_text, required_skills, min_experience=0):
        # Store custom skills for this screening
        self.custom_skills = [skill for skill in required_skills 
                             if not any(skill.lower() in pattern[0].lower() 
                                      for pattern in self.lang_patterns)]
        
        # Extract skills and experience from CV
        cv_skills = self.extract_skills(cv_text)
        cv_experience = self.extract_experience(cv_text)
        
        # Skill variations for matching
        skill_aliases = {
            'java': ['java', 'core java', 'java se', 'java ee'],
            'javascript': ['javascript', 'js', 'node.js', 'nodejs'],
            'python': ['python', 'py', 'python3'],
            'sql': ['sql', 'mysql', 'postgresql', 'oracle', 'sqlite'],
            'html': ['html', 'html5'],
            'css': ['css', 'css3', 'scss'],
            'ruby': ['ruby', 'rails', 'ruby on rails'],
            'c++': ['c++', 'cpp'],
            'c#': ['c#', 'csharp', '.net'],
            'react': ['react', 'reactjs'],
            'angular': ['angular', 'angularjs'],
            'node.js': ['node.js', 'nodejs', 'node'],
            'git': ['git', 'github'],
            'docker': ['docker', 'container'],
            'aws': ['aws', 'amazon web services'],
            'azure': ['azure', 'microsoft azure']
        }
        
        # Find matched skills
        matched_skills = []
        for required_skill in required_skills:
            req_skill_lower = required_skill.lower()
            
            # Direct match
            if any(skill.lower() == req_skill_lower for skill in cv_skills):
                matched_skills.append(required_skill)
                continue
            
            # Check aliases
            for base_skill, aliases in skill_aliases.items():
                if req_skill_lower in aliases:
                    if any(cv_skill.lower() in aliases for cv_skill in cv_skills):
                        matched_skills.append(required_skill)
                        break
        
        # Calculate scores
        skill_score = len(matched_skills) / len(required_skills) if required_skills else 0
        experience_score = 1.0 if cv_experience >= min_experience else cv_experience / max(min_experience, 1)
        
        # Calculate final score (60% skills, 40% experience)
        final_score = (skill_score * 0.6) + (experience_score * 0.4)
        
        return final_score, matched_skills

    def extract_text(self, file_path):
        """Extract text from various file formats"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension == '.pdf':
                return self.extract_text_from_pdf(file_path)
            elif file_extension == '.docx':
                return self.extract_text_from_docx(file_path)
            elif file_extension == '.txt':
                return self.extract_text_from_txt(file_path)
            else:
                print(f"Unsupported file format: {file_extension}")
                return ""
        except Exception as e:
            print(f"Error extracting text from {file_path}: {str(e)}")
            return ""

    def extract_text_from_txt(self, file_path):
        """Extract text from TXT files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try different encodings if UTF-8 fails
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception as e:
                print(f"Error reading TXT file: {str(e)}")
                return ""

    def extract_text_from_docx(self, file_path):
        """Extract text from DOCX files"""
        try:
            import docx
            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n'.join(full_text)
        except Exception as e:
            print(f"Error reading DOCX file: {str(e)}")
            return ""

    def screen_cvs(self, cvs, job_requirements):
        results = []
        required_skills = []
        min_experience = 0
        
        for line in job_requirements.split('\n'):
            line = line.strip()
            if line.startswith('- '):
                if 'years of experience' in line.lower():
                    try:
                        min_experience = int(line.split()[1])
                    except:
                        pass
                elif not any(keyword in line.lower() for keyword in ['experience', 'education']):
                    required_skills.append(line[2:].strip())
        
        # Process each CV
        for cv in cvs:
            try:
                cv_text = self.extract_text(cv['file_path'])
                if cv_text:
                    score, matched_skills = self.calculate_match_score(cv_text, required_skills, min_experience)
                    result = {
                        'candidate_name': cv['candidate_name'],
                        'score': score,
                        'file_path': cv['file_path'],
                        'matched_skills': matched_skills
                    }
                    results.append(result)
            except Exception as e:
                continue
        
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results 