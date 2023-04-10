'use strict'


// --------------FORM JS------------------
// Form user can fill out for media completion.

function showSuggestions() {
    var searchTerm = document.getElementById("searchBox").value;
    console.log('searchTerm');
    console.log(searchTerm);
    fetch(`/api/suggestions?query=${searchTerm}`)
        .then(response => response.json())
        .then(suggestions => displaySuggestions(suggestions))
        .catch(error => console.error(error));
}

function displaySuggestions(suggestions) {
    var modal = document.getElementById("myModal");
    var suggestionList = document.getElementById("suggestionList");
    suggestionList.innerHTML = "";
    for (var i = 0; i < suggestions.length; i++) {
        var suggestion = suggestions[i];
        var suggestionDiv = document.createElement("div");
        suggestionDiv.addEventListener("click", function (event) {
            var title = event.currentTarget.querySelector(".suggestion-title").innerHTML;
            var summary = event.currentTarget.querySelector(".suggestion-summary").innerHTML;
            document.getElementById("summary-box").value = summary;
            modal.style.display = "none";
        });
        suggestionDiv.className = "suggestion";
        var suggestionTitle = document.createElement("div");
        suggestionTitle.className = "suggestion-title";
        suggestionTitle.innerHTML = suggestion.title;
        suggestionDiv.appendChild(suggestionTitle);
        var suggestionSummary = document.createElement("div");
        suggestionSummary.className = "suggestion-summary";
        suggestionSummary.innerHTML = suggestion.summary;
        suggestionDiv.appendChild(suggestionSummary);
        suggestionList.appendChild(suggestionDiv);
    }
    modal.style.display = "block";
    var closeBtn = document.getElementsByClassName("close")[0];
    closeBtn.onclick = function () {
        modal.style.display = "none";
    }
}

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
            } else {
                window.location.href = "http://localhost:5000/profile"
            };
        });
});



