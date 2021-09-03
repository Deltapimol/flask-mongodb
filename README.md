## Flask MongoDB POC

# **Note: dev branch has the most recent changes**

**API Endpoints**

<ol>
<li>Create user => localhost:5000/user</li>

        Request Body =
        {
            "name": "Anmol Shinde",
            "email": "anmolshinde106@gmail.com",
            "password": "12345"
        }
<br>
<li>Get user => localhost:5000/user/{id}</li>
     <br>
<li>List all users => localhost:5000/users</li>
     <br>
<li>Update user => localhost:5000/user/{id} </li>

        Request Body =
        {
            "name": "Anmol Shinde",
            "email": "anmolshinde108@gmail.com",
            "password": "12345"
        }

<br>
<li>Delete a user => localhost:5000/user/{id}</li>
</ol>
