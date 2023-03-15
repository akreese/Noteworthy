'use strict'


// --------------FORM JS------------------
// Form user can fill out for media completion.

document.getElementById('new_form').addEventListener('submit', (evt) => {
    evt.preventDefault();

    const formInputs = {
        name: document.querySelector('input[name="name"]').value,
        mediaType: document.querySelector('#type').value,
        category: document.querySelector('input[name="category"]').value,
        summary: document.querySelector('input[name="summary"]').value,
        rating: document.querySelector('#rating').value,
        thoughts: document.querySelector('input[name="thoughts"]').value,
        recommend: document.querySelector('#recommend_or_not').value,
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



