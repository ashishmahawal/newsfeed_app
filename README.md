### create a user in DB
```
CREATE USER testuser with password 'password';
ALTER ROLE testuser CREATEDB;
```


### Following tables should exist in SQL DB newsfeed

```
CREATE TABLE image (
    imageId VARCHAR(255) PRIMARY KEY,
    postId VARCHAR(255),
    userId VARCHAR(255),
    createdAt varchar(255),
    location VARCHAR(255),
    tags VARCHAR(255)
);
```

```
CREATE TABLE users (
    userId VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255),
    email VARCHAR(255),
    contact VARCHAR(20)
);
```

```
CREATE TABLE post (
    postId VARCHAR(255) PRIMARY KEY,
    userId VARCHAR(255),
    text TEXT,
    createdAt VARCHAR(255)
);
```