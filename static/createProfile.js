'use strict'


//-------------CREATE PROFILE JS------------------
// New User creation/button 

const newUserSubmit = document.querySelector('#new_user_button');
const newUserForm = document.getElementById("new_user_form");
const newUserFormFname = newUserForm.querySelector('input[name="fname"]');
const newUserFormLname = newUserForm.querySelector('input[name="lname"]');
const newUserFormEmail = newUserForm.querySelector('input[name="email"]');
const newUserFormPassword = newUserForm.querySelector('input[name="password"]');
const newUserFormRePassword = newUserForm.querySelector('input[name="password_2"]');

function createNewUser(event) {
    const newUserEmail = newUserFormEmail.value;
    const url = `/api/createUser`;
    fetch(url, {
        method: "POST",        
        body: JSON.stringify({
            title: "foo",
            body: "bar",
            userId: 1
        }),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    })
    .then((response) => response.json())
    .then((responseData) => {
        if (!responseData.success) {
            alert(responseData.message);
        } else {
            window.location.href = "http://localhost:5000/profile"
        }
    });
    event.preventDefault(); 
};
newUserForm.addEventListener('submit', createNewUser);