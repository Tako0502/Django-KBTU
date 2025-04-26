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
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import { Add, Search, Person, BusinessCenter } from '@mui/icons-material';
import { jobs, candidates } from '../services/api';

const RecruiterDashboard = () => {
  const [jobsList, setJobsList] = useState([]);
  const [candidatesList, setCandidatesList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [openJobDialog, setOpenJobDialog] = useState(false);
  const [newJob, setNewJob] = useState({
    title: '',
    description: '',
    requirements: '',
    location: '',
  });

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const [jobsRes, candidatesRes] = await Promise.all([
        jobs.getJobListings(),
        candidates.getCandidates()
      ]);
      setJobsList(jobsRes);
      setCandidatesList(candidatesRes);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleJobSubmit = async () => {
    try {
      await jobs.createJob(newJob);
      setOpenJobDialog(false);
      setNewJob({ title: '', description: '', requirements: '', location: '' });
      fetchDashboardData();
    } catch (err) {
      setError('Failed to create job posting');
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
              startIcon={<Add />}
              onClick={() => setOpenJobDialog(true)}
            >
              Post New Job
            </Button>
            <Button
              variant="contained"
              startIcon={<Search />}
              onClick={() => window.location.href = '/candidate-search'}
            >
              Search Candidates
            </Button>
          </Paper>
        </Grid>

        {/* Jobs Overview */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Job Postings
              </Typography>
              <List>
                {jobsList.slice(0, 5).map((job) => (
                  <ListItem key={job.id}>
                    <ListItemText
                      primary={job.title}
                      secondary={`${job.location} - ${job.company}`}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Candidates Overview */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Candidates
              </Typography>
              <List>
                {candidatesList.slice(0, 5).map((candidate) => (
                  <ListItem key={candidate.id}>
                    <ListItemText
                      primary={`${candidate.user.first_name} ${candidate.user.last_name}`}
                      secondary={`${candidate.experience} years experience`}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* New Job Dialog */}
      <Dialog open={openJobDialog} onClose={() => setOpenJobDialog(false)}>
        <DialogTitle>Post New Job</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            name="title"
            label="Job Title"
            fullWidth
            value={newJob.title}
            onChange={(e) => setNewJob({...newJob, title: e.target.value})}
          />
          <TextField
            margin="dense"
            name="description"
            label="Description"
            fullWidth
            multiline
            rows={4}
            value={newJob.description}
            onChange={(e) => setNewJob({...newJob, description: e.target.value})}
          />
          <TextField
            margin="dense"
            name="requirements"
            label="Requirements"
            fullWidth
            multiline
            rows={4}
            value={newJob.requirements}
            onChange={(e) => setNewJob({...newJob, requirements: e.target.value})}
          />
          <TextField
            margin="dense"
            name="location"
            label="Location"
            fullWidth
            value={newJob.location}
            onChange={(e) => setNewJob({...newJob, location: e.target.value})}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenJobDialog(false)}>Cancel</Button>
          <Button onClick={handleJobSubmit} variant="contained">Post Job</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default RecruiterDashboard; 