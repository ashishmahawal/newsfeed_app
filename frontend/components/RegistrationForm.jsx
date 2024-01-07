// components/RegistrationForm.js
import React, { useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/router';

const RegistrationForm = () => {
  const router = useRouter();
  const [formData, setFormData] = useState({
    userId: '',
    password: '',
    email: '',
    contact: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:3001/v1/user/create', formData);
      console.log(response.data);

      // Redirect to login page after successful registration
      router.push('/login');
    } catch (error) {
      console.error('Error registering user:', error);
    }
  };

  return (
    <div>
      <h2>Sign Up</h2>
      <form onSubmit={handleSubmit}>
        <label>
          User ID:
          <input type="text" name="userId" value={formData.userId} onChange={handleChange} />
        </label>
        <br />
        <label>
          Password:
          <input type="password" name="password" value={formData.password} onChange={handleChange} />
        </label>
        <br />
        <label>
          Email:
          <input type="email" name="email" value={formData.email} onChange={handleChange} />
        </label>
        <br />
        <label>
          Contact:
          <input type="text" name="contact" value={formData.contact} onChange={handleChange} />
        </label>
        <br />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default RegistrationForm;
