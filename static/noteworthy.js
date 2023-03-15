'use strict'


// --------------HOMEPAGE JS------------------
// Login information/button 

const loginButton = document.querySelector('#login_button');
const form = document.getElementById("login_form");
const formEmail = form.querySelector('input[name="email"]');
const formPassword = form.querySelector('input[name="password"]');

function validateUser(event){
    const userEmail = formEmail.value;
    const userPassword = formPassword.value
    const url = `/api/validateUser?email=${userEmail}&password=${userPassword}`;
    fetch(url)
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
form.addEventListener('submit', validateUser);


// Create new profile button

const createLoginButton = document.querySelector('#create_button');
function handleClick() {
    window.location.href = "http://localhost:5000/createprofile"
};
createLoginButton.addEventListener('click', handleClick);

