// frontenc/src/pages/validationSchema.js

import * as yup from 'yup';

export const validationSchema = yup.object({
  email: yup
    .string()
    .email('Enter a valid email')
    .required('Email is required'),
  password_hash: yup
    .string()
    .min(8, 'Password should be of minimum 8 characters length')
    .required('Password is required'),
  firstname: yup
    .string()
    .required('First name is required'),
  lastname: yup
    .string()
    .required('Last name is required'),
  terms: yup
    .boolean()
    .oneOf([true], 'You must accept the terms and conditions')
});