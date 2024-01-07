// components/LoginForm.js
import React, { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/router';
import { Button, TextField, Typography, Container, CssBaseline, Avatar } from '@mui/material';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

const LoginForm = () => {
  const classes = useStyles();
  const router = useRouter();
  const [formData, setFormData] = useState({
    userId: '',
    password: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    try {
        console.log(formData)
      const response = await axios.post('http://localhost:8000/v1/user/login', formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      if (response.status === 202) {
        console.log('Login successful!');
  
        // Redirect to the homepage (assuming the route is '/')
        router.push('/');
      } else {
        console.error('Login failed. Invalid credentials or other error.');
      }
    } catch (error) {
      console.error('Error logging in:', error);
    }
  };
  

  return (
    <Container component="main" maxWidth="md"> {/* Increase maxWidth to 'md' */}
      <CssBaseline />
      <div className={classes.paper}>
        <Avatar className={classes.avatar}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign in
        </Typography>
        <form className={classes.form} onSubmit={handleSubmit}>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="userId"
            label="User ID"
            name="userId"
            autoComplete="userId"
            autoFocus
            value={formData.userId}
            onChange={handleChange}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            autoComplete="current-password"
            value={formData.password}
            onChange={handleChange}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            Sign In
          </Button>
        </form>
      </div>
    </Container>
  );
};

export default LoginForm;

