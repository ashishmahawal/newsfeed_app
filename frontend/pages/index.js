// pages/index.js
import Head from 'next/head';
import { Container } from 'react-bootstrap';
import PostForm from '../components/PostForm';
import UserPosts from '../components/UserPosts';

const Home = () => {
  const handlePostSuccess = () => {
    // Refresh user posts after uploading
    // You can implement this based on your needs
    console.log('Post success, refresh user posts');
  };

  return (
    <Container>
      <Head>
        <title>News Feed App</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <h1>News Feed App</h1>
        <PostForm onPostSuccess={handlePostSuccess} />
        <UserPosts />
      </main>
    </Container>
  );
};

export default Home;
