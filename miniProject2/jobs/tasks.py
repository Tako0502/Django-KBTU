from celery import shared_task
from .models import JobApplication, JobMatch, JobListing
from resumes.models import Resume
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

logger = logging.getLogger(__name__)

@shared_task
def calculate_job_match(application_id):
    try:
        application = JobApplication.objects.get(id=application_id)
        job = application.job
        resume = application.resume
        
        # Calculate skills match
        job_skills = set(job.skills)
        resume_skills = set(resume.skills)
        skills_match = list(job_skills.intersection(resume_skills))
        skills_match_score = len(skills_match) / len(job_skills) if job_skills else 0
        
        # Calculate requirements match using TF-IDF
        job_requirements = ' '.join(job.requirements)
        resume_text = f"{resume.education} {resume.experience}"
        
        vectorizer = TfidfVectorizer()
        try:
            tfidf_matrix = vectorizer.fit_transform([job_requirements, resume_text])
            requirements_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except ValueError:
            requirements_similarity = 0
        
        # Calculate overall match score
        match_score = (skills_match_score * 0.6 + requirements_similarity * 0.4) * 100
        
        # Create or update job match
        job_match, created = JobMatch.objects.get_or_create(
            job=job,
            resume=resume,
            defaults={
                'match_score': match_score,
                'skills_match': skills_match,
                'requirements_match': job.requirements
            }
        )
        
        if not created:
            job_match.match_score = match_score
            job_match.skills_match = skills_match
            job_match.requirements_match = job.requirements
            job_match.save()
        
        # Update application match score
        application.match_score = match_score
        application.save()
        
        return {
            'status': 'success',
            'application_id': application_id,
            'match_score': match_score
        }
        
    except JobApplication.DoesNotExist:
        logger.error(f"Job application with id {application_id} not found")
        return {
            'status': 'error',
            'message': f"Job application with id {application_id} not found"
        }
    except Exception as e:
        logger.error(f"Error calculating job match for application {application_id}: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        }

@shared_task
def find_matching_jobs(resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
        active_jobs = JobListing.objects.filter(is_active=True)
        
        for job in active_jobs:
            # Create a job application to trigger match calculation
            application = JobApplication.objects.create(
                job=job,
                applicant=resume.user,
                resume=resume,
                status='applied'
            )
            # Calculate match score
            calculate_job_match.delay(application.id)
        
        return {
            'status': 'success',
            'resume_id': resume_id,
            'jobs_processed': active_jobs.count()
        }
        
    except Resume.DoesNotExist:
        logger.error(f"Resume with id {resume_id} not found")
        return {
            'status': 'error',
            'message': f"Resume with id {resume_id} not found"
        }
    except Exception as e:
        logger.error(f"Error finding matching jobs for resume {resume_id}: {str(e)}")
        return {
            'status': 'error',
            'message': str(e)
        } 