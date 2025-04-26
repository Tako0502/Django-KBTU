import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Alert,
} from '@mui/material';
import { Upload, Description, Work, Assessment } from '@mui/icons-material';
import axios from 'axios';

const JobSeekerDashboard = () => {
  const [resumes, setResumes] = useState([]);
  const [jobMatches, setJobMatches] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    setLoading(true);
    try {
      const [resumesRes, matchesRes] = await Promise.all([
        axios.get('/api/resumes/analyses/'),
        axios.get('/api/jobs/matches/')
      ]);
      setResumes(resumesRes.data.results);
      setJobMatches(matchesRes.data.results);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleResumeUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('resume_file', file);

    try {
      await axios.post('/api/resumes/upload/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      fetchUserData();
    } catch (err) {
      setError('Failed to upload resume');
      console.error(err);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      
      <Grid container spacing={3}>
        {/* Quick Actions */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              startIcon={<Upload />}
              component="label"
            >
              Upload Resume
              <input
                type="file"
                hidden
                accept=".pdf,.doc,.docx"
                onChange={handleResumeUpload}
              />
            </Button>
            <Button
              variant="contained"
              startIcon={<Work />}
              onClick={() => window.location.href = '/job-search'}
            >
              Search Jobs
            </Button>
          </Paper>
        </Grid>

        {/* Resume Analysis */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <Description /> Your Resumes
              </Typography>
              <List>
                {resumes.map((resume) => (
                  <ListItem key={resume.id}>
                    <ListItemText
                      primary={`Resume #${resume.id}`}
                      secondary={`Score: ${resume.overall_score}/100 | Uploaded: ${new Date(resume.created_at).toLocaleDateString()}`}
                    />
                  </ListItem>
                ))}
                {resumes.length === 0 && (
                  <ListItem>
                    <ListItemText primary="No resumes uploaded yet" />
                  </ListItem>
                )}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Job Matches */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <Assessment /> Job Matches
              </Typography>
              <List>
                {jobMatches.map((match) => (
                  <ListItem key={match.id}>
                    <ListItemText
                      primary={match.job_title}
                      secondary={`Match Score: ${match.match_score}% | ${match.matched_skills.length} skills matched`}
                    />
                  </ListItem>
                ))}
                {jobMatches.length === 0 && (
                  <ListItem>
                    <ListItemText primary="No job matches found" />
                  </ListItem>
                )}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default JobSeekerDashboard; 