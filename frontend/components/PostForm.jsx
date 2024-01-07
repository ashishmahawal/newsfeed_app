// components/PostForm.js
import React, { useState } from 'react';
import { Button, TextField, Typography, Paper, Grid } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import axios from 'axios';

const PostForm = ({ onPostSuccess }) => {
  const [postText, setPostText] = useState('');
  const [imageFile, setImageFile] = useState(null);

  const handlePost = async () => {
    const formData = new FormData();
    formData.append('text', postText);
    formData.append('userId', 'user123'); // Replace with the actual user ID
    formData.append('file', imageFile);
    formData.append('location','palwal')
    formData.append('tags','ai')

    try {
      const response = await axios.post('http://localhost:8000/v1/image/upload', formData);
      if (response.status === 200) {
        console.log('Post uploaded successfully');
        onPostSuccess();
        setPostText('');
        setImageFile(null);
      } else {
        console.error('Failed to upload post');
      }
    } catch (error) {
      console.error('Error uploading post:', error);
    }
  };

  const handleImageChange = (e) => {
    setImageFile(e.target.files[0]);
  };

  return (
    <Paper elevation={3} style={{ padding: '20px', maxWidth: '600px', margin: '20px auto' }}>
      <Typography variant="h5">Create a Post</Typography>
      <form>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12}>
            <TextField
              fullWidth
              variant="outlined"
              label="Post Text"
              multiline
              rows={3}
              value={postText}
              onChange={(e) => setPostText(e.target.value)}
            />
          </Grid>
          <Grid item xs={12}>
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              style={{ display: 'none' }}
              id="imageInput"
            />
            <label htmlFor="imageInput">
              <Button
                variant="outlined"
                component="span"
                startIcon={<CloudUploadIcon />}
              >
                Upload Image
              </Button>
            </label>
          </Grid>
          <Grid item xs={12}>
            <Button variant="contained" color="primary" onClick={handlePost}>
              Post
            </Button>
          </Grid>
        </Grid>
      </form>
    </Paper>
  );
};

export default PostForm;
