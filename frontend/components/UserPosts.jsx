// components/UserPosts.js
import React, { useEffect, useState } from 'react';
import { Card, CardContent, Typography, Grid } from '@mui/material';
import axios from 'axios';
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
    card: {
        maxWidth: 360,
        margin: '10px auto',
        backgroundColor: theme.palette.background.paper,
      },
      text: {
        fontSize: '1.8rem', // Adjust text size as needed
        marginBottom: theme.spacing(1),
      },
      image: {
        width: '100%', // Keep the image width at 100%
        height: 'auto', // Auto-calculate height to maintain aspect ratio
      },
}));

const UserPosts = () => {
  const classes = useStyles();
  const [userPosts, setUserPosts] = useState([]);

  useEffect(() => {
    const fetchUserPosts = async () => {
      const userId = 'user123'; // Replace with the actual user ID
      try {
        const response = await axios.get(`http://localhost:8000/v1/user/${userId}`);
        if (response.status === 200) {
          setUserPosts(response.data.posts);
        } else {
          console.error('Failed to fetch user posts');
        }
      } catch (error) {
        console.error('Error fetching user posts:', error);
      }
    };

    fetchUserPosts();
  }, []);

  return (
    <div>
      {userPosts.map((post) => (
        <Card key={post.postId} className={classes.card}>
          <Grid container>
            <Grid item xs={12}>
              <CardContent>
                <Typography variant="h6" className={classes.text}>{post.text}</Typography>
              </CardContent>
            </Grid>
            <Grid item xs={12}>
              <img
                src={`http://localhost:8000/v1/image/${post.imageId}`}
                alt="Post"
                style={{ width: '100%', height: 'auto' }}
                className={classes.image}
              />
            </Grid>
            <Grid item xs={12}>
              <CardContent>
                <Typography variant="subtitle2" color="textSecondary">
                  {post.createAt}
                </Typography>
              </CardContent>
            </Grid>
          </Grid>
        </Card>
      ))}
    </div>
  );
};

export default UserPosts;
