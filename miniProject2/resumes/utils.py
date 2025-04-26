import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

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

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file."""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'
            return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        raise

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

def extract_skills(text: str) -> List[str]:
    """Extract skills from text using NLTK."""
    # Common skills keywords
    skill_keywords = {
        'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin'],
        'web': ['html', 'css', 'react', 'angular', 'vue', 'django', 'flask', 'node.js'],
        'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis'],
        'devops': ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'ci/cd'],
        'data': ['machine learning', 'data science', 'pandas', 'numpy', 'tensorflow', 'pytorch'],
        'mobile': ['android', 'ios', 'react native', 'flutter'],
        'cloud': ['aws', 'azure', 'gcp', 'cloud computing'],
        'tools': ['git', 'jenkins', 'jira', 'confluence']
    }
    
    tokens = preprocess_text(text)
    skills = []
    
    for category, keywords in skill_keywords.items():
        for keyword in keywords:
            if keyword in ' '.join(tokens):
                skills.append(keyword)
    
    return list(set(skills))

def extract_education(text: str) -> List[str]:
    """Extract education information from text."""
    education_patterns = [
        r'(?i)(?:bachelor|master|phd|doctorate)[\s\w]*\s(?:in|of)\s[\w\s]+',
        r'(?i)(?:b\.?s\.?|m\.?s\.?|ph\.?d\.?)[\s\w]*\s(?:in|of)\s[\w\s]+',
        r'(?i)(?:university|college|institute)[\s\w]+'
    ]
    
    education = []
    for pattern in education_patterns:
        matches = re.findall(pattern, text)
        education.extend(matches)
    
    return list(set(education))

def extract_experience(text: str) -> List[Dict]:
    """Extract work experience from text."""
    experience_pattern = r'(?i)(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s\d{4}\s*[-–]\s*(?:present|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s\d{4})'
    
    experiences = []
    matches = re.finditer(experience_pattern, text)
    
    for match in matches:
        date_range = match.group()
        # Extract the text after the date range until the next date range or end
        end_pos = text.find('\n', match.end())
        if end_pos == -1:
            end_pos = len(text)
        description = text[match.end():end_pos].strip()
        
        experiences.append({
            'date_range': date_range,
            'description': description
        })
    
    return experiences

def analyze_resume(file_path: str) -> Dict:
    """Analyze a resume file and extract relevant information."""
    try:
        # Check if file is PDF by extension
        if not file_path.lower().endswith('.pdf'):
            raise ValueError("Only PDF files are supported")
        
        # Extract text
        text = extract_text_from_pdf(file_path)
        
        # Extract information
        skills = extract_skills(text)
        education = extract_education(text)
        experience = extract_experience(text)
        
        return {
            'skills': skills,
            'education': education,
            'experience': experience,
            'raw_text': text
        }
    except Exception as e:
        logger.error(f"Error analyzing resume: {str(e)}")
        raise 