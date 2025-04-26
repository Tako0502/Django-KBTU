import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Box,
  CircularProgress,
  Alert,
  Chip,
  Stack,
} from '@mui/material';
import { Search, School, WorkHistory } from '@mui/icons-material';
import { candidates } from '../services/api';

const CandidateSearch = () => {
  const [candidatesList, setCandidatesList] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({
    search: '',
    skills: '',
    experience: ''
  });

  const fetchCandidates = async () => {
    setLoading(true);
    try {
      const response = await candidates.getCandidates(filters);
      // Handle both array and object with results property
      const candidatesData = Array.isArray(response) ? response : response.results || [];
      setCandidatesList(candidatesData);
      setError(null);
    } catch (err) {
      setError('Failed to fetch candidates. Please try again later.');
      console.error('Error fetching candidates:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCandidates();
  }, []);

  const handleFilterChange = (event) => {
    const { name, value } = event.target;
    setFilters(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSearch = (event) => {
    event.preventDefault();
    fetchCandidates();
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <form onSubmit={handleSearch}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  name="search"
                  label="Keywords"
                  value={filters.search}
                  onChange={handleFilterChange}
                  InputProps={{
                    startAdornment: <Search sx={{ mr: 1, color: 'text.secondary' }} />
                  }}
                />
              </Grid>
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  name="skills"
                  label="Skills"
                  value={filters.skills}
                  onChange={handleFilterChange}
                  InputProps={{
                    startAdornment: <School sx={{ mr: 1, color: 'text.secondary' }} />
                  }}
                />
              </Grid>
              <Grid item xs={12} md={2}>
                <TextField
                  fullWidth
                  name="experience"
                  label="Min. Experience"
                  type="number"
                  value={filters.experience}
                  onChange={handleFilterChange}
                  InputProps={{
                    startAdornment: <WorkHistory sx={{ mr: 1, color: 'text.secondary' }} />
                  }}
                />
              </Grid>
              <Grid item xs={12} md={2}>
                <Button
                  type="submit"
                  variant="contained"
                  fullWidth
                  sx={{ height: '100%' }}
                >
                  Search
                </Button>
              </Grid>
            </Grid>
          </form>
        </CardContent>
      </Card>

      {loading ? (
        <Box display="flex" justifyContent="center" my={4}>
          <CircularProgress />
        </Box>
      ) : (
        <Grid container spacing={3}>
          {Array.isArray(candidatesList) && candidatesList.length > 0 ? (
            candidatesList.map((candidate) => (
              <Grid item xs={12} key={candidate.id}>
                <Card>
                  <CardContent>
                    <Typography variant="h5" gutterBottom>
                      {candidate.user?.first_name} {candidate.user?.last_name}
                    </Typography>
                    <Stack direction="row" spacing={1} mb={2}>
                      {Array.isArray(candidate.skills) && candidate.skills.map((skill) => (
                        <Chip key={skill} label={skill} />
                      ))}
                    </Stack>
                    <Typography variant="body1" paragraph>
                      Experience: {candidate.experience} years
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Education: {candidate.education}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))
          ) : (
            <Grid item xs={12}>
              <Alert severity="info">No candidates found matching your criteria.</Alert>
            </Grid>
          )}
        </Grid>
      )}
    </Container>
  );
};

export default CandidateSearch; 