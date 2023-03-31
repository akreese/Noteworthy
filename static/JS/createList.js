'use strict'

// ----------SEARCH COMPLETED FORMS JS-------------
// Allowing user to search completed forms through the search bar

// document.getElementById('search_bar').addEventListener('click', (evt) => {
//     evt.preventDefault();
// });

// ----------CREATE LIST JS------------------
// Creating a new list with input from new list form


document.getElementById('new_list').addEventListener('submit', (evt) => {
    evt.preventDefault();
    const nameInput = {
        name : document.querySelector('input[name="name').value,
    };
    fetch('/createList', {
        method: 'POST',
        body:JSON.stringify(nameInput),
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then((response) => response.json())
        .then((responseJson) => {
            if (!reponseJson.success) {
                alert(reponseJson.message);
            }else{
                alert(reponseJson.message);
            };
            });
        });

// ----------------ADD BUTTONS FOR ADDING FORMS TO LIST--------------------
function addToList(buttonElement) {
    const requestBody = {
        selectedFormId: buttonElement.id
    }
    fetch('/addFormToList', {
        method: 'POST',
        body: JSON.stringify(requestBody),
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then((response) => response.json())
        .then((responseJson) => {
            if (!responseJson.success) {
                alert(responseJson.message);
            }
        });
    };  



// ----------BUTTON TO GO BACK TO PROFILE WHEN LIST IS FINISHED-------

const finishedButton = document.querySelector('#finished_button');
function handleClick() {
    window.location.href = "http://localhost:5000/profile"
};
finishedButton.addEventListener('click', handleClick);
