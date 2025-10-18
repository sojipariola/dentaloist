// frontend/src/pages/Register.js

import React from 'react';
import { Container, Paper, Typography, Box } from '@mui/material';
import RegisterForm from './RegisterForm';

const Register = () => {
  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 8 }}>
        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom align="center">
            Register
          </Typography>
          <Typography>Registration Form </Typography>
          <RegisterForm />
        </Paper>
      </Box>
    </Container>
  );
};

export default Register;