// Author Jahziel Belmonte
// NOTE THIS IS CODE I USED FOR ASSIGNMENT 3 FOR INDIVIDUAL ASSIGNMENT
// THIS CODE IS NOT FOR DISTRIBUTION FOR OTHER MEMBERS
// Copying or modifying this code is plagiarism and will be reported to the course coordinator
/*
    Login form code -
 */
// This code is used to validate the login form and send the data to the server

// Get the CSRF token from the cookie to use in the AJAX request
// reference https://stackoverflow.com/questions/10730362/get-cookie-by-name
function getCookie(name) {
    let cookieValue = null;
    // If the cookie is not set, return null
    if (document.cookie && document.cookie !== '') {
        // Split the cookie string into an array of cookies
        const cookies = document.cookie.split(';');
        // Loop through the cookies and find the one we want
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue =  decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$(document).ready(function () {
    console.log("Form.js loaded");
    validateForm();
});

function ReservedCharacters(obj) {
    if (obj.includes("root") || obj.includes("Root") || obj.includes("ROOT")
        || obj.includes("\\") || obj.includes("/") || obj.includes(":")
        || obj.includes("*") || obj.includes("?") || obj.includes("\"")
        || obj.includes(";") || obj.includes("|") || obj.includes("<")) {
        alert(obj + " contains reserved characters");
        return;
    } else {
        return;
    }
}

function validateForm() {
    //check if form is present
    let form = document.getElementById("login-form");

    form.addEventListener("submit", function (event) {
        //prevent form from submitting
        event.preventDefault();

        //GET FORM VALUES
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        //check if values are filled
        if (!username || !password ) {
            alert("Please fill in all fields");
            return;
        }
        //usernames must be at least 3 characters
        if (username.length < 3) {
            alert("Username must be at least 3 characters");
            return;
        }
    });

    //validate form
    $("#login-form").validate({
        rules: {
            username: {
                required: true,
                minlength: 3
            },
            password: {
                required: true,
                minlength: 4
            },
        },
        messages: {
            username: {
                required: "Please enter your username",
                minlength: "Your username must consist of at least 3 characters"
            },
            password: {
                required: "Please provide a password",
                minlength: "Your password must be at least 4 characters long"
            },
        },
        submitHandler: function (form) {
            //submit the form
            $.ajax({
                type: "POST",
                url: "/Login/",
                headers: {
                    "X-CSRFToken": csrftoken
                },
                mode: "same-origin",

                data: {
                    username: $("#username").val(),
                    password: $("#password").val(),
                },
                success: function (response) {
                    //handle success
                    alert("Checking login authentication");
                },
                error: function (response) {
                    //handle error
                    console.log("Error logging in", response);
                    alert("Error logging in");
                },
            })
        }
    });
}
