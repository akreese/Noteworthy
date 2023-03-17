'use strict'


// ------------USER'S PROFILE---------------
// User's profile and its functions 


// Create new media form

const createFormButton = document.querySelector('#new_form');
function handleClick() {
    window.location.href = "http://localhost:5000/newForm"
};
createFormButton.addEventListener('click', handleClick);


// Create new list

// const createListButton = document.querySelector('#new_list');
// function handleClick() {
//     window.location.href = "http://localhost:5000/"
// };
// createListButton.addEventListener('click', handleClick);


// View Lists
