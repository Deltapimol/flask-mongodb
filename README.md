# Flask MongoDB POC

**API Endpoints**

### Users collection APIs
<ol>
<li>Create user => {hostname}:5000/api/v1/users/user</li>

        Request Body =
        {
            "name": "Anmol Shinde",
            "email": "anmolshinde106@gmail.com",
            "password": "12345"
        }
<br>
<li>Get user => {hostname}:5000/api/v1/users/user/</li>
     <br>
<li>List all users => {hostname}:5000/api/v1/users</li>
     <br>
        Request Body =
        {
            "name": "Anmol Shinde",
            "email": "anmolshinde108@gmail.com",
            "password": "12345"
        }

<br>
<li>Delete a user => {hostname}:5000/api/v1/users/user/{id}</li>
</ol>

### Blogs collection APIs

<ol>
<li>Add blog => {hostname}:5000/api/v1/blogs</li>
        
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
<li>Update blog =>{hostname}:5000/api/v1/blogs/{blog_id}</li>
        
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
<li>Get all blogs =>{hostname}:5000/api/v1/blogs</li>
<br>
<li>Get blog by blog id => {hostname}:5000/api/v1/blogs/{blog_id}</li>
<br>
<li>Delete blog by blog id => {hostname}:5000/api/v1/blogs/{blog_id}</li>
<br>
<li> Get blogs by user id => {hostname}:5000/api/v1/blogs/user/{user_id} <br> Get all published blogs by user id => {hostname}:5000/api/v1/blogs/user/{user_id}?published=true <br>Get all unpublished blogs by user id => {hostname}:5000/api/v1/blogs/user/{user_id}?published=false</li>
</ol>

