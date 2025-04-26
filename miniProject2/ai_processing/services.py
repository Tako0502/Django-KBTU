import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict, List, Optional
from resumes.models import Resume, ResumeAnalysis
from jobs.models import JobListing
from celery import shared_task
from .models import JobMatch

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

def preprocess_text(text: str) -> List[str]:
    """Preprocess text by tokenizing, removing stopwords, and lemmatizing."""
    # Tokenize
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords and non-alphabetic tokens
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
    
    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return tokens

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts using TF-IDF and cosine similarity."""
    # Preprocess texts
    tokens1 = preprocess_text(text1)
    tokens2 = preprocess_text(text2)
    
    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform([' '.join(tokens1), ' '.join(tokens2)])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except ValueError:
        return 0.0

def match_resume_with_job(resume_id: int, job_id: int) -> Dict:
    """Match a resume with a job and return match details."""
    try:
        resume = Resume.objects.get(id=resume_id)
        job = JobListing.objects.get(id=job_id)
        analysis = ResumeAnalysis.objects.get(resume=resume)
        
        # Calculate skill match
        resume_skills = set(analysis.skills)
        job_skills = set(job.required_skills)
        skill_match = len(resume_skills.intersection(job_skills)) / len(job_skills) if job_skills else 0
        
        # Calculate description similarity
        description_similarity = calculate_similarity(
            analysis.raw_text,
            f"{job.title} {job.description} {job.requirements}"
        )
        
        # Calculate overall match score
        match_score = (skill_match + description_similarity) / 2
        
        return {
            'match_score': match_score,
            'skills_match': list(resume_skills.intersection(job_skills)),
            'missing_skills': list(job_skills - resume_skills),
            'description_similarity': description_similarity
        }
    except (Resume.DoesNotExist, JobListing.DoesNotExist, ResumeAnalysis.DoesNotExist) as e:
        return {
            'error': str(e),
            'match_score': 0.0,
            'skills_match': [],
            'missing_skills': [],
            'description_similarity': 0.0
        }

def analyze_resume_content(resume_id: int) -> Dict:
    """Analyze resume content and return analysis results."""
    try:
        resume = Resume.objects.get(id=resume_id)
        analysis = ResumeAnalysis.objects.get(resume=resume)
        
        # Preprocess text
        tokens = preprocess_text(analysis.raw_text)
        
        # Calculate basic metrics
        word_count = len(tokens)
        unique_words = len(set(tokens))
        avg_word_length = sum(len(word) for word in tokens) / len(tokens) if tokens else 0
        
        return {
            'word_count': word_count,
            'unique_words': unique_words,
            'avg_word_length': avg_word_length,
            'processed_text': ' '.join(tokens)
        }
    except (Resume.DoesNotExist, ResumeAnalysis.DoesNotExist) as e:
        return {
            'error': str(e),
            'word_count': 0,
            'unique_words': 0,
            'avg_word_length': 0,
            'processed_text': ''
        }

@shared_task
def analyze_resume(resume_analysis_id):
    resume_analysis = ResumeAnalysis.objects.get(id=resume_analysis_id)
    
    # Extract text based on file type
    file_extension = resume_analysis.resume_file.name.split('.')[-1].lower()
    if file_extension == 'pdf':
        text = resume_analysis.extract_text_from_pdf(resume_analysis.resume_file)
    elif file_extension in ['docx', 'doc']:
        text = resume_analysis.extract_text_from_docx(resume_analysis.resume_file)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")
    
    # Extract information
    resume_analysis.skills = resume_analysis.extract_skills(text)
    resume_analysis.education = resume_analysis.extract_education(text)
    resume_analysis.experience = resume_analysis.extract_experience(text)
    
    # Analyze resume
    resume_analysis.overall_score = calculate_overall_score(resume_analysis)
    resume_analysis.ats_compatibility = check_ats_compatibility(text)
    resume_analysis.formatting_score = analyze_formatting(text)
    
    # Generate recommendations
    resume_analysis.skill_gaps = identify_skill_gaps(resume_analysis.skills)
    resume_analysis.formatting_suggestions = generate_formatting_suggestions(text)
    resume_analysis.keyword_suggestions = suggest_keywords(text)
    
    resume_analysis.save()
    return resume_analysis_id

def calculate_overall_score(resume_analysis):
    # Implement scoring logic
    return 0.0

def check_ats_compatibility(text):
    # Implement ATS compatibility check
    return 0.0

def analyze_formatting(text):
    # Implement formatting analysis
    return 0.0

def identify_skill_gaps(skills):
    # Implement skill gap analysis
    return []

def generate_formatting_suggestions(text):
    # Implement formatting suggestions
    return []

def suggest_keywords(text):
    # Implement keyword suggestions
    return []

@shared_task
def match_resume_with_job(resume_analysis_id, job_description):
    resume_analysis = ResumeAnalysis.objects.get(id=resume_analysis_id)
    
    # Calculate match score
    match_score = calculate_match_score(resume_analysis.skills, job_description)
    
    # Create job match
    job_match = JobMatch.objects.create(
        resume_analysis=resume_analysis,
        job_description=job_description,
        match_score=match_score,
        matched_skills=find_matching_skills(resume_analysis.skills, job_description),
        missing_skills=find_missing_skills(resume_analysis.skills, job_description)
    )
    
    return job_match.id

def calculate_match_score(skills, job_description):
    # Implement match score calculation
    return 0.0

def find_matching_skills(skills, job_description):
    # Implement skill matching
    return []

def find_missing_skills(skills, job_description):
    # Implement missing skills identification
    return [] 