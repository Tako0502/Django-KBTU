# AI-Powered Resume Analyzer

An intelligent resume analysis platform that helps job seekers improve their resumes and matches them with suitable job opportunities. The platform uses AI and NLP to analyze resumes, provide feedback, and match candidates with relevant job listings.

## Features

- Resume upload and parsing (PDF, DOCX)
- AI-powered resume analysis and feedback
- Skill gap analysis
- ATS (Applicant Tracking System) compatibility scoring
- Job matching based on skills and requirements
- Multi-database architecture for optimal performance
- JWT-based authentication
- Role-based access control (Job Seeker, Recruiter, Admin)
- API documentation with Swagger/OpenAPI

## Tech Stack

### Backend
- Django 4+
- Django Rest Framework
- Celery for async tasks
- Redis for caching
- PostgreSQL for user data
- MongoDB for resume storage
- MySQL for logging
- spaCy and NLTK for NLP
- scikit-learn for job matching

### Frontend (To be implemented)
- React/Next.js
- Tailwind CSS
- Redux for state management

## Prerequisites

- Python 3.8+
- PostgreSQL
- MongoDB
- MySQL
- Redis
- Node.js and npm (for frontend)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/resume-analyzer.git
cd resume-analyzer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install spaCy model:
```bash
python -m spacy download en_core_web_sm
```

5. Create a `.env` file in the project root with the following variables:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/resume_analyzer
MONGODB_URI=mongodb://localhost:27017/resume_analyzer
MYSQL_DB=resume_analyzer
MYSQL_USER=root
MYSQL_PASSWORD=your-mysql-password
MYSQL_HOST=localhost
MYSQL_PORT=3306
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
FRONTEND_URL=http://localhost:3000
```

6. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

7. Create a superuser:
```bash
python manage.py createsuperuser
```

## Running the Application

1. Start Redis:
```bash
redis-server
```

2. Start Celery worker:
```bash
celery -A resume_analyzer worker -l info
```

3. Start Celery beat (for scheduled tasks):
```bash
celery -A resume_analyzer beat -l info
```

4. Run the development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`
API documentation will be available at `http://localhost:8000/swagger/`

## API Endpoints

### Authentication
- POST `/api/auth/register/` - User registration
- POST `/api/auth/login/` - User login
- POST `/api/auth/refresh/` - Refresh JWT token
- POST `/api/auth/verify-email/` - Email verification
- POST `/api/auth/reset-password/` - Password reset

### Resumes
- GET `/api/resumes/` - List user's resumes
- POST `/api/resumes/` - Upload new resume
- GET `/api/resumes/{id}/` - Get resume details
- PUT `/api/resumes/{id}/` - Update resume
- DELETE `/api/resumes/{id}/` - Delete resume
- GET `/api/resumes/{id}/analysis/` - Get resume analysis

### Jobs
- GET `/api/jobs/listings/` - List job postings
- POST `/api/jobs/listings/` - Create job posting
- GET `/api/jobs/listings/{id}/` - Get job details
- POST `/api/jobs/listings/{id}/apply/` - Apply for job
- GET `/api/jobs/applications/` - List job applications
- GET `/api/jobs/matches/` - Get job matches

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- spaCy for NLP capabilities
- scikit-learn for machine learning algorithms
- Django and DRF for the robust backend framework
- Celery for async task processing 