'use strict'



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
            // console.log(responseData.message);
            if (!responseData.success) {
                // console.log('FALSE');
                alert(responseData.message);
            } else {
                window.location.href = "http://localhost:5000/profile"
            }

            // document.querySelector('#email').innerText = responseData['email'];
            // document.querySelector('#password').innerText = responseData['password'];
            // if ('success' == False) {
            //     return flash("The email and/or password you have entered was incorrect");
            // } else {
            //     return flash("Welcome back!");
            // };
    });
    event.preventDefault(); 
};
form.addEventListener('submit', validateUser);



