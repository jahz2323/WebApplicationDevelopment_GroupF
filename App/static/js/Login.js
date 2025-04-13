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
// Get the CSRF token from the cookie for AJAX LOGIN, prevent CSRF error
const csrftoken = getCookie('csrftoken');

// Call the validateForm function when the document is ready - listen for the submit event
$(document).ready(function () {
    console.log("Form.js loaded");
    validateForm();
});

// Check if either the user or pass input contains defined characters , if so alert and reject the auth
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

    //When submit button is clicked validate the form and then run the submit handler for AJAX POST
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
        // Define the rules for validation
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
        // Define the error messages
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
            /* submit the form POST to serverside for authentication at /Login/, response.POST.data {
                username,
                password
            } */

            $.ajax({
                // Set the type of request to POST
                // Set the URL to send the request to
                // Set the headers to include the CSRF token
                // Set the mode to same-origin to prevent CORS errors
                // Set the data to send to the server
                // Set the success and error functions to handle the response
                type: "POST",
                url: "/Login/",
                headers: {
                    "X-CSRFToken": csrftoken // Prevent restricted error
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
