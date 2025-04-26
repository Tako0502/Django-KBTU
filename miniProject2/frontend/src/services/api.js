import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const auth = {
  login: (credentials) => api.post('/auth/login/', credentials),
  register: (userData) => api.post('/auth/register/', userData),
  logout: () => api.post('/auth/logout/'),
  getCurrentUser: () => api.get('/auth/profile/'),
};

export const jobs = {
  getJobListings: (filters = {}) => api.get('/jobs/listings/', { params: filters }),
  getJobDetails: (id) => api.get(`/jobs/listings/${id}/`),
  applyToJob: (id) => api.post(`/jobs/listings/${id}/apply/`),
};

export const resumes = {
  uploadResume: (formData) => api.post('/resumes/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  }),
  getResumes: () => api.get('/resumes/'),
  getResumeAnalysis: (id) => api.get(`/resumes/${id}/analysis/`),
};

export const candidates = {
  getCandidates: (filters = {}) => api.get('/candidates/', { params: filters }),
  getCandidateDetails: (id) => api.get(`/candidates/${id}/`),
  updateCandidate: (id, data) => api.put(`/candidates/${id}/`, data),
};

export default {
  auth,
  jobs,
  resumes,
  candidates,
}; 