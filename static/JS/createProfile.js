'use strict'


//-------------CREATE PROFILE JS------------------
// New User creation/button 


document.getElementById('new_user_form').addEventListener('submit', (evt) => {
    evt.preventDefault();

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