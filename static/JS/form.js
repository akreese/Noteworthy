'use strict'


// --------------FORM JS------------------
// Form user can fill out for media completion.

function showSuggestions() {
    var searchTerm = document.getElementById("searchBox").value;
    var searchType = document.getElementById("type-select").value;
    fetch(`/api/suggestions?type=${searchType}&query=${searchTerm}`)
        .then(response => response.json())
        .then(suggestions => displaySuggestions(suggestions))
        .catch(error => console.error(error));
}

function displaySuggestions(suggestions) {
    var modal = document.getElementById("myModal");
    var suggestionList = document.getElementById("suggestionList");
    suggestionList.innerHTML = "";
    if (suggestions.length > 0) {
        for (var i = 0; i < suggestions.length; i++) {
            var suggestion = suggestions[i];
            var suggestionDiv = document.createElement("div");
            suggestionDiv.addEventListener("click", function (event) {
                var title = event.currentTarget.querySelector(".suggestion-title").innerHTML;
                var summary = event.currentTarget.querySelector(".suggestion-summary").innerHTML;
                var category = event.currentTarget.querySelector(".suggestion-category").innerHTML;

                document.getElementById("summary-box").value = summary;
                document.getElementById("category-box").value = category;
                document.getElementById("searchBox").value = title;
                modal.style.display = "none";
            });
            suggestionDiv.className = "suggestion";
            var suggestionTitle = document.createElement("div");
            suggestionTitle.className = "suggestion-title";
            suggestionTitle.innerHTML = suggestion.title;
            suggestionDiv.appendChild(suggestionTitle);
            var suggestionCategory = document.createElement("div");
            suggestionCategory.className = "suggestion-category";
            suggestionCategory.innerHTML = suggestion.category;
            suggestionDiv.appendChild(suggestionCategory);
            suggestionList.appendChild(suggestionDiv);
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
    } else {
        alert('No suggestion found, please continue filling out the form');

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



