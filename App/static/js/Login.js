// Author Jahziel Belmonte

/*
    Login form code -
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
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
