import re
import logging
import PyPDF2
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import os

class ResumeAnalyzer:
    """Class for analyzing resumes and extracting key information"""
    
    def __init__(self):
        """Initialize the analyzer with required NLP tools"""
        self.setup_nltk()
        self.setup_spacy()
        self.skills_keywords = self.load_skills_keywords()
        
    def setup_nltk(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        self.stop_words = set(stopwords.words('english'))
    
    def setup_spacy(self):
        """Load spaCy model"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logging.warning("spaCy model not found. Using basic NLP processing.")
            self.nlp = None
    
    def load_skills_keywords(self):
        """Load common skills keywords for extraction"""
        return {
            'programming': [
                'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
                'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql', 'html', 'css', 'typescript'
            ],
            'frameworks': [
                'react', 'angular', 'vue', 'django', 'flask', 'spring', 'express',
                'node.js', 'bootstrap', 'jquery', 'laravel', 'rails', 'asp.net'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle',
                'cassandra', 'elasticsearch', 'dynamodb'
            ],
            'tools': [
                'git', 'docker', 'kubernetes', 'jenkins', 'aws', 'azure', 'gcp',
                'terraform', 'ansible', 'jira', 'confluence', 'slack'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'problem-solving',
                'analytical', 'creative', 'adaptable', 'organized', 'detail-oriented'
            ]
        }
    
    def extract_text_from_pdf(self, file_path):
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            logging.error(f"Error extracting text from PDF: {str(e)}")
            return None
    
    def extract_text_from_txt(self, file_path):
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    return file.read()
            except Exception as e:
                logging.error(f"Error reading text file: {str(e)}")
                return None
        except Exception as e:
            logging.error(f"Error reading text file: {str(e)}")
            return None
    
    def extract_contact_info(self, text):
        """Extract contact information from text"""
        contact_info = {}
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        contact_info['email'] = emails[0] if emails else None
        
        # Extract phone number
        phone_pattern = r'(\+?1?[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})'
        phones = re.findall(phone_pattern, text)
        if phones:
            phone = ''.join(phones[0])
            contact_info['phone'] = phone
        else:
            contact_info['phone'] = None
        
        # Extract name (first line that looks like a name)
        lines = text.split('\n')
        name = None
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and len(line.split()) <= 4 and len(line) > 2:
                # Simple heuristic: if it's not too long and contains letters
                if re.match(r'^[A-Za-z\s.]+$', line):
                    name = line
                    break
        
        contact_info['name'] = name
        return contact_info
    
    def extract_skills(self, text):
        """Extract skills from text"""
        text_lower = text.lower()
        found_skills = []
        
        # Check for each skill category
        for category, skills in self.skills_keywords.items():
            for skill in skills:
                if skill.lower() in text_lower:
                    found_skills.append(skill)
        
        # Remove duplicates and return
        return list(set(found_skills))
    
    def extract_education(self, text):
        """Extract education information"""
        education = []
        
        # Common degree patterns
        degree_patterns = [
            r'bachelor[\'s]?\s+(?:of\s+)?(?:science|arts|engineering|business)',
            r'master[\'s]?\s+(?:of\s+)?(?:science|arts|engineering|business)',
            r'phd|ph\.d|doctorate',
            r'associate[\'s]?\s+degree',
            r'b\.?s\.?|b\.?a\.?|m\.?s\.?|m\.?a\.?|m\.?b\.?a\.?'
        ]
        
        for pattern in degree_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                education.append(match.strip())
        
        return list(set(education))
    
    def extract_experience(self, text):
        """Extract work experience information"""
        experience = []
        
        # Look for common experience indicators
        experience_patterns = [
            r'(\d+)\s*(?:\+)?\s*years?\s+(?:of\s+)?experience',
            r'experience[:\s]*(\d+)\s*(?:\+)?\s*years?',
            r'(\d+)\s*(?:\+)?\s*yrs?\s+(?:of\s+)?(?:experience|exp)'
        ]
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                experience.append(f"{match} years of experience")
        
        return experience
    
    def analyze_resume(self, file_path):
        """Main method to analyze a resume file"""
        try:
            # Extract text based on file type
            if file_path.lower().endswith('.pdf'):
                text = self.extract_text_from_pdf(file_path)
            elif file_path.lower().endswith('.txt'):
                text = self.extract_text_from_txt(file_path)
            else:
                logging.error(f"Unsupported file type: {file_path}")
                return None
            
            if not text:
                logging.error("Failed to extract text from file")
                return None
            
            # Extract information
            contact_info = self.extract_contact_info(text)
            skills = self.extract_skills(text)
            education = self.extract_education(text)
            experience = self.extract_experience(text)
            
            # Create resume data structure
            resume_data = {
                'name': contact_info.get('name'),
                'email': contact_info.get('email'),
                'phone': contact_info.get('phone'),
                'skills': skills,
                'education': education,
                'experience': experience,
                'raw_text': text,
                'word_count': len(text.split()),
                'skill_count': len(skills)
            }
            
            logging.info(f"Resume analysis completed. Found {len(skills)} skills.")
            return resume_data
            
        except Exception as e:
            logging.error(f"Error analyzing resume: {str(e)}")
            return None
