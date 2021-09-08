# Flask MongoDB POC

**API Endpoints**

### Users collection APIs
<ol>
<li>Create user (POST) => {hostname}:5000/api/v1/users/user</li>

        Request Body =
        {
            "name": "Anmol Shinde",
            "email": "anmolshinde106@gmail.com",
            "password": "12345"
        }
<br>
<li>Get user (GET) => {hostname}:5000/api/v1/users/user/{user_id}</li>
<br>
<li>Update user (PUT) => {hostname}:5000/api/v1/users/user</li>
        
        Request Body =
        {   "id": "61373438296c1274940e638b"
            "name": "Anmol Shinde",
            "email": "anmolshinde108@gmail.com",
            "password": "12345"
        }
   
<br>
<li>Delete a user (DELETE) => {hostname}:5000/api/v1/users/user/{id}</li>
<br>
<li>List all users (GET) => {hostname}:5000/api/v1/users</li>
</ol>

### Blogs collection APIs

<ol>
<li>Add blog (POST) => {hostname}:5000/api/v1/blogs</li>
        
        Request Body =
        {
        "author": "Anmol Shinde",
        "email": "anmolshinde13@gmail.com",
        "title": "Blog title",
        "text": "Blog text",
        "publish": false
        }
        
        # Pass publish = True to publish the blog
<br>
<li>Update blog (PUT) =>{hostname}:5000/api/v1/blogs/{blog_id}</li>
        
        Request Body =
        {
            "author": "Anmol Ankush Shinde",
            "email": "anmolshinde13@gmail.com",
            "title": "Blog title updated",
            "text": "Blog Text updated",
            "publish": false
        }
        
        # Pass publish = True to publish the blog
<br>
<li>Toggle publish/unpublish blog (PATCH) => {hostname}:5000/api/v1/blogs/toggle-publish/{blog_id}</li>
<br>
<li>Get all blogs (GET) =>{hostname}:5000/api/v1/blogs</li>
<br>
<li>Get blog by blog id (GET) => {hostname}:5000/api/v1/blogs/{blog_id}</li>
<br>
<li>Delete blog by blog id (DELETE) => {hostname}:5000/api/v1/blogs/{blog_id}</li>
<br>
<li> Get blogs by user id (GET) => {hostname}:5000/api/v1/blogs/user/{user_id} <br> Get all published blogs by user id (GET) => {hostname}:5000/api/v1/blogs/user/{user_id}?published=true <br>Get all unpublished blogs by user id GET) => {hostname}:5000/api/v1/blogs/user/{user_id}?published=false</li>
</ol>

### Coments collection APIs

<ol>
<li>Add a comment (POST) => {hostname}:5000/api/v1/comments</li>

        Request Body = 
        {
            "email": "anmolshinde13@gmail.com",
            "comment": "Blog comment 3",
            "blog_id": "61373438296c1274940e638b"
        }

<br>
<li>Update a comment (PUT) => {hostname}:5000/api/v1/comments/{comment_id} </li>

        Request Body = 
        {
            "comment_id": "61373438296c1274940e638b",
            "comment": "Blog comment edited",
            "blog_id": "61373438296c1274940e638b"
        }

<br>
<li>Delete a comment (DELETE) => {hostname}:5000/api/v1/comments/{comment_id}</li>
<br>
<li>Add a reply to a comment (POST) => {hostname}:5000/api/v1/comments/reply</li>
        
        Request Body = 
        {
            "email": "anmolshinde13@gmail.com",
            "reply": "Blog comment 3",
            "comment_id": "61374cce7b0bc9854d34e065"
        }

<br>
<li>Edit a reply (PUT) => {hostname}:5000/api/v1/comments/reply</li>

        Request Body =
        {
            "email": "anmolshinde106@gmail.com",
            "reply": "This is an updated reply",
            "comment_id": "61374cce7b0bc9854d34e065",
            "reply_id": "6138a1760a9809d20d9afd1b"
        }

<li>Delete a reply (DELETE) => {hostname}:5000/api/v1/comments/{comment_id}/reply/{reply_id}</li>
</ol>
