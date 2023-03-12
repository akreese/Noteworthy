'use strict'


//-------------CREATE PROFILE JS------------------
// New User creation/button 

// const newUserSubmit = document.querySelector('#new_user_button');
// const newUserForm = document.getElementById("new_user_form");
// const newUserFormFname = newUserForm.querySelector('input[name="fname"]');
// const newUserFormLname = newUserForm.querySelector('input[name="lname"]');
// const newUserFormEmail = newUserForm.querySelector('input[name="email"]');
// const newUserFormPassword = newUserForm.querySelector('input[name="password"]');
// const newUserFormRePassword = newUserForm.querySelector('input[name="password_2"]');

document.getElementById('new_user_form').addEventListener('submit', (evt) => {
    evt.preventDefault();
    // console.log('HERE');
    // console.log(document.querySelector('input[name="fname"]').value);
    // console.log(document.querySelector('input[name="lname"]').value);
    // console.log(document.querySelector('input[name="email"]').value);
    // console.log(document.querySelector('input[name="password"]').value);
    // console.log(document.querySelector('input[name="password_2"]').value);



    const formInputs = {
        fname: document.querySelector('input[name="fname"]').value,
        lname: document.querySelector('input[name="lname"]').value,
        email: document.querySelector('input[name="email"]').value,
        password: document.querySelector('input[name="password"]').value,
        rePassword: document.querySelector('input[name="password_2"]').value,
    };
    fetch('/api/createUser', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then((response) => response.json())
        .then((responseJson) => {
            if (!responseJson.success) {
                alert(responseJson.message);
        } else {
            window.location.href = "http://localhost:5000/profile"
        };
        });
});