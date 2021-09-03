# Flask MongoDB POC

**API Endpoints**

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
<li>Update user => {hostname}:5000/api/v1/users/user/{id} </li>

        Request Body =
        {
            "name": "Anmol Shinde",
            "email": "anmolshinde108@gmail.com",
            "password": "12345"
        }

<br>
<li>Delete a user => {hostname}:5000/api/v1/users/user/{id}</li>
</ol>
