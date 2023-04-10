'use strict'


// --------------FORM JS------------------
// Form user can fill out for media completion.

document.getElementById('new_form').addEventListener('submit', (evt) => {
    evt.preventDefault();


    const formInputs = {
        name: document.querySelector('input[name="name"]').value,
        mediaType: document.querySelector('#type-select').value,
        category: document.querySelector('input[name="category"]').value,
        summary: document.querySelector('textarea[name="summary"]').value,
        rating: document.querySelector('#rate-select').value,
        thoughts: document.querySelector('textarea[name="thoughts"]').value,
        recommend: document.querySelector('#rec-select').value,
    };
    fetch('/createForm', {
        method: 'POST',
        body: JSON.stringify(formInputs),
        headers: {
            'Content-Type': 'application/json'
        },
    })
        .then((response) => response.json())
        .then((reponseJson) => {
            if (!reponseJson.success) {
                alert(reponseJson.message);
            }else {
                window.location.href = "http://localhost:5000/profile"
            };
            });
        });



