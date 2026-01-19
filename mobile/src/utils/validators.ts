import * as Yup from 'yup';

export const loginValidationSchema = Yup.object().shape({
  username: Yup.string()
    .required('Username is required')
    .min(3, 'Username must be at least 3 characters')
    .max(50, 'Username must be less than 50 characters'),
  password: Yup.string()
    .required('Password is required')
    .min(6, 'Password must be at least 6 characters'),
});

export const registerValidationSchema = Yup.object().shape({
  username: Yup.string()
    .required('Username is required')
    .min(3, 'Username must be at least 3 characters')
    .max(50, 'Username must be less than 50 characters')
    .matches(/^[a-zA-Z0-9_]+$/, 'Username can only contain letters, numbers, and underscores'),
  email: Yup.string()
    .required('Email is required')
    .email('Invalid email address'),
  password: Yup.string()
    .required('Password is required')
    .min(6, 'Password must be at least 6 characters')
    .max(100, 'Password must be less than 100 characters'),
  confirmPassword: Yup.string()
    .required('Please confirm your password')
    .oneOf([Yup.ref('password')], 'Passwords must match'),
});

export const scrapeValidationSchema = Yup.object().shape({
  url: Yup.string()
    .required('URL is required')
    .url('Must be a valid URL'),
  merchant: Yup.string()
    .required('Merchant is required'),
  max_pages: Yup.number()
    .min(1, 'Must be at least 1 page')
    .max(10, 'Maximum 10 pages allowed')
    .integer('Must be a whole number'),
});

export const inventoryItemValidationSchema = Yup.object().shape({
  title: Yup.string()
    .required('Title is required')
    .min(3, 'Title must be at least 3 characters')
    .max(200, 'Title must be less than 200 characters'),
  price: Yup.number()
    .required('Price is required')
    .min(0, 'Price must be positive'),
  quantity: Yup.number()
    .required('Quantity is required')
    .min(0, 'Quantity must be positive')
    .integer('Quantity must be a whole number'),
  merchant: Yup.string()
    .required('Merchant is required'),
});

export const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const isValidUrl = (url: string): boolean => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

export const isValidPrice = (price: number): boolean => {
  return !isNaN(price) && price >= 0;
};
