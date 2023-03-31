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

const createListButton = document.querySelector('#new_list');
function handleClick2() {
    window.location.href = "http://localhost:5000/newList"
};
createListButton.addEventListener('click', handleClick2);


// Allow users to view their lists.


function fetchProfile(buttonElement) {
    // const url = `http://localhost:5000/viewLists?name=${buttonElement.id}`
    const url = "http://localhost:5000/viewLists/" + buttonElement.id

    window.location.href = url
    // console.log(buttonElement.id)
};
