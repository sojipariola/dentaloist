// frontend/src/pages/RegisterForm.js
import React from 'react';
import { useFormik } from 'formik';
import {
  TextField,
  Button,
  Box,
  FormControlLabel,
  Checkbox
} from '@mui/material';
import { validationSchema } from './validationSchema';

const RegisterForm = () => {
  const formik = useFormik({
    initialValues: {
      email: '',
      password_hash: '',
      firstname: '',
      lastname: '',
      terms: false
    },
    validationSchema: validationSchema,
    onSubmit: (values) => {
      // Handle form submission
      console.log(values);
    },
  });

  return (
    <form onSubmit={formik.handleSubmit}>
      <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
        <TextField
          fullWidth
          id="firstname"
          name="firstname"
          label="First Name"
          value={formik.values.firstname}
          onChange={formik.handleChange}
          error={formik.touched.firstname && Boolean(formik.errors.firstname)}
          helperText={formik.touched.firstname && formik.errors.firstname}
        />
        <TextField
          fullWidth
          id="lastname"
          name="lastname"
          label="Last Name"
          value={formik.values.lastname}
          onChange={formik.handleChange}
          error={formik.touched.lastname && Boolean(formik.errors.lastname)}
          helperText={formik.touched.lastname && formik.errors.lastname}
        />
      </Box>
      <TextField
        fullWidth
        id="email"
        name="email"
        label="Email"
        value={formik.values.email}
        onChange={formik.handleChange}
        error={formik.touched.email && Boolean(formik.errors.email)}
        helperText={formik.touched.email && formik.errors.email}
        sx={{ mb: 2 }}
      />
      <TextField
        fullWidth
        id="password_hash"
        name="password_hash"
        label="Password"
        type="password"
        value={formik.values.password_hash}
        onChange={formik.handleChange}
        error={formik.touched.password_hash && Boolean(formik.errors.password_hash)}
        helperText={formik.touched.password_hash && formik.errors.password_hash}
        sx={{ mb: 2 }}
      />
      <FormControlLabel
        control={
          <Checkbox
            id="terms"
            name="terms"
            checked={formik.values.terms}
            onChange={formik.handleChange}
          />
        }
        label="I agree to the terms and conditions"
        sx={{ mb: 2 }}
      />
      <Button color="primary" variant="contained" fullWidth type="submit">
        Register
      </Button>
    </form>
  );
};

export default RegisterForm;