import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import { useAuth } from '../context/AuthContext';

const Profile = () => {
  const { user } = useAuth();

  return (
    <Container>
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Profile
        </Typography>
        <Typography>Email: {user?.email}</Typography>
        <Typography>Role: {user?.role}</Typography>
      </Box>
    </Container>
  );
};

export default Profile;