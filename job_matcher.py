import logging
import re
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logging.warning("sentence-transformers not available. Using keyword-based matching only.")
import numpy as np

class JobMatcher:
    """Class for matching resumes with job descriptions"""
    
    def __init__(self):
        """Initialize the job matcher with sentence transformer model"""
        self.model = None
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                # Use a lightweight sentence transformer model
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                logging.info("Sentence transformer model loaded successfully")
            except Exception as e:
                logging.error(f"Error loading sentence transformer: {str(e)}")
                self.model = None
        else:
            logging.info("Using keyword-based matching (sentence-transformers not available)")
    
    def preprocess_text(self, text):
        """Preprocess text for better matching"""
        if not text:
            return ""
        
        # Convert to lowercase and remove extra whitespace
        text = re.sub(r'\s+', ' ', text.lower().strip())
        
        # Remove special characters but keep letters, numbers, and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        
        return text
    
    def extract_keywords(self, text):
        """Extract important keywords from text"""
        if not text:
            return []
        
        # Simple keyword extraction based on word frequency
        words = text.lower().split()
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
            'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Return unique keywords
        return list(set(keywords))
    
    def calculate_keyword_overlap(self, resume_keywords, job_keywords):
        """Calculate keyword overlap between resume and job"""
        if not resume_keywords or not job_keywords:
            return 0.0
        
        resume_set = set(resume_keywords)
        job_set = set(job_keywords)
        
        intersection = resume_set.intersection(job_set)
        union = resume_set.union(job_set)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def calculate_semantic_similarity(self, resume_text, job_text):
        """Calculate semantic similarity using sentence transformers"""
        if not self.model:
            logging.warning("Sentence transformer model not available, using keyword matching only")
            return 0.0
        
        try:
            # Preprocess texts
            resume_clean = self.preprocess_text(resume_text)
            job_clean = self.preprocess_text(job_text)
            
            if not resume_clean or not job_clean:
                return 0.0
            
            # Generate embeddings
            embeddings = self.model.encode([resume_clean, job_clean])
            
            # Calculate cosine similarity
            similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            
            return float(similarity)
            
        except Exception as e:
            logging.error(f"Error calculating semantic similarity: {str(e)}")
            return 0.0
    
    def generate_feedback(self, resume_data, job_data, similarity_score):
        """Generate improvement feedback for the resume"""
        feedback = []
        
        # Get job requirements and skills
        job_text = f"{job_data['description']} {job_data['requirements']}"
        job_keywords = self.extract_keywords(job_text)
        
        # Get resume skills and keywords
        resume_text = resume_data.get('raw_text', '')
        resume_keywords = self.extract_keywords(resume_text)
        resume_skills = [skill.lower() for skill in resume_data.get('skills', [])]
        
        # Find missing important keywords
        missing_keywords = []
        for keyword in job_keywords:
            if keyword not in resume_keywords and keyword not in resume_skills:
                missing_keywords.append(keyword)
        
        # Provide feedback based on similarity score
        if similarity_score < 0.3:
            feedback.append("Your resume has low compatibility with this job. Consider highlighting more relevant skills and experience.")
        elif similarity_score < 0.5:
            feedback.append("Your resume shows moderate compatibility. Consider emphasizing relevant experience more prominently.")
        elif similarity_score < 0.7:
            feedback.append("Your resume shows good compatibility with this job. Minor improvements could increase your match score.")
        else:
            feedback.append("Excellent match! Your resume aligns well with the job requirements.")
        
        # Suggest missing skills
        if missing_keywords:
            top_missing = missing_keywords[:5]  # Top 5 missing keywords
            feedback.append(f"Consider highlighting these relevant skills/keywords: {', '.join(top_missing)}")
        
        # Check for contact information
        if not resume_data.get('email'):
            feedback.append("Make sure your email address is clearly visible on your resume.")
        
        if not resume_data.get('phone'):
            feedback.append("Consider adding your phone number for easy contact.")
        
        # Check resume length
        word_count = resume_data.get('word_count', 0)
        if word_count < 200:
            feedback.append("Your resume might be too short. Consider adding more details about your experience and achievements.")
        elif word_count > 800:
            feedback.append("Your resume might be too long. Consider being more concise and focusing on the most relevant information.")
        
        return feedback
    
    def match_resume_to_job(self, resume_data, job_data):
        """Match a resume to a job and return detailed results"""
        try:
            # Prepare texts for comparison
            resume_text = resume_data.get('raw_text', '')
            job_text = f"{job_data['description']} {job_data['requirements']}"
            
            # Calculate different similarity metrics
            semantic_similarity = self.calculate_semantic_similarity(resume_text, job_text)
            
            # Calculate keyword overlap
            resume_keywords = self.extract_keywords(resume_text)
            job_keywords = self.extract_keywords(job_text)
            keyword_overlap = self.calculate_keyword_overlap(resume_keywords, job_keywords)
            
            # Calculate overall similarity score (weighted average)
            overall_similarity = (semantic_similarity * 0.7) + (keyword_overlap * 0.3)
            
            # Generate feedback
            feedback = self.generate_feedback(resume_data, job_data, overall_similarity)
            
            # Create match result
            match_result = {
                'job_id': job_data['id'],
                'job_title': job_data['title'],
                'company': job_data['company'],
                'location': job_data.get('location', 'Not specified'),
                'salary': job_data.get('salary', 'Not specified'),
                'similarity_score': round(overall_similarity * 100, 1),  # Convert to percentage
                'semantic_similarity': round(semantic_similarity * 100, 1),
                'keyword_overlap': round(keyword_overlap * 100, 1),
                'feedback': feedback,
                'matched_skills': list(set(resume_keywords).intersection(set(job_keywords)))[:10],  # Top 10 matched skills
                'match_level': self.get_match_level(overall_similarity)
            }
            
            logging.info(f"Job match calculated: {match_result['job_title']} - {match_result['similarity_score']}%")
            return match_result
            
        except Exception as e:
            logging.error(f"Error matching resume to job: {str(e)}")
            return None
    
    def get_match_level(self, similarity_score):
        """Get match level based on similarity score"""
        if similarity_score >= 0.7:
            return "Excellent"
        elif similarity_score >= 0.5:
            return "Good"
        elif similarity_score >= 0.3:
            return "Moderate"
        else:
            return "Low"
