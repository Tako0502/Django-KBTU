from celery import shared_task
from django.conf import settings
from .models import Resume, ResumeAnalysis, ResumeFeedback, JobMatch
from .utils import analyze_resume, extract_text_from_pdf
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_resume(resume_id):
    """Process a resume file and extract text."""
    try:
        resume = Resume.objects.get(id=resume_id)
        text = extract_text_from_pdf(resume.file.path)
        resume.extracted_text = text
        resume.save()
        return True
    except Exception as e:
        logger.error(f"Error processing resume {resume_id}: {str(e)}")
        return False

@shared_task
def analyze_resume_task(resume_id):
    """Analyze a resume and create analysis record."""
    try:
        resume = Resume.objects.get(id=resume_id)
        analysis = analyze_resume(resume.file.path)
        
        # Create or update analysis record
        ResumeAnalysis.objects.update_or_create(
            resume=resume,
            defaults={
                'skills': analysis['skills'],
                'education': analysis['education'],
                'experience': analysis['experience'],
                'raw_text': analysis['raw_text']
            }
        )
        return True
    except Exception as e:
        logger.error(f"Error analyzing resume {resume_id}: {str(e)}")
        return False

@shared_task
def generate_feedback(resume_id):
    """Generate feedback for a resume."""
    try:
        resume = Resume.objects.get(id=resume_id)
        analysis = analyze_resume(resume.file.path)
        
        # Create feedback record
        feedback = ResumeFeedback.objects.create(
            resume=resume,
            skills_feedback=", ".join(analysis['skills']),
            education_feedback=", ".join(analysis['education']),
            experience_feedback=str(analysis['experience'])
        )
        return feedback.id
    except Exception as e:
        logger.error(f"Error generating feedback for resume {resume_id}: {str(e)}")
        return None

@shared_task
def match_job(resume_id, job_id):
    """Match a resume with a job."""
    try:
        resume = Resume.objects.get(id=resume_id)
        analysis = analyze_resume(resume.file.path)
        
        # Create job match record
        match = JobMatch.objects.create(
            resume=resume,
            job_id=job_id,
            match_score=0.0,  # This should be calculated based on actual matching logic
            skills_match=analysis['skills'],
            requirements_match=[]
        )
        return match.id
    except Exception as e:
        logger.error(f"Error matching resume {resume_id} with job {job_id}: {str(e)}")
        return None

@shared_task
def process_resume_analysis(resume_id):
    """Process and analyze a resume in one task."""
    try:
        if process_resume(resume_id):
            return analyze_resume_task(resume_id)
        return False
    except Exception as e:
        logger.error(f"Error in process_resume_analysis for resume {resume_id}: {str(e)}")
        return False 