// Wait for the entire DOM content to be fully loaded before executing any script logic
document.addEventListener("DOMContentLoaded", () => {
    // Get all tab buttons for navigation across steps (e.g., Basic Info, Role Selection, Confirmation)
    const tabs = Array.from(document.querySelectorAll("#formTabs button"));

    // Get all role cards (e.g., Manager, Technician, etc.)
    const roleCards = document.querySelectorAll(".role-card");

    // Hidden input to store the selected role's value for form submission
    const selectedRole = document.getElementById("selectedRole");

    // Reference to the entire registration form
    const form = document.getElementById("registrationForm");

   
    // ROLE CARD SELECTION HIGHLIGHT
   
    // For each role card, add a click event to mark it as selected
    roleCards.forEach(card => {
        card.addEventListener("click", () => {
            // Remove selection styling from all cards
            roleCards.forEach(c => c.classList.remove("border-primary", "bg-opacity-75", "selected"));
            // Add highlight classes to the clicked card
            card.classList.add("border-primary", "bg-opacity-75", "selected");
            // Update the hidden input with the selected role value
            selectedRole.value = card.dataset.role;
        });
    });

   
    // TAB SWITCHING FUNCTION
   
    // Function to switch between tabs by tabId (e.g., "role", "basic", "confirmation")
    function goTo(tabId) {
        // Remove 'active' class from all tabs
        tabs.forEach(btn => btn.classList.remove("active"));

        // Add 'active' class to the currently selected tab
        document.querySelector(`[data-bs-target="#${tabId}"]`).classList.add("active");

        // Hide all tab panes
        document.querySelectorAll(".tab-pane").forEach(tab => tab.classList.remove("show", "active"));

        // Show only the selected tab pane
        document.getElementById(tabId).classList.add("show", "active");
    }

   
    // BUTTON EVENT HANDLERS FOR NAVIGATION
   
    // Go to the Role Selection tab when "Next" is clicked from Basic Info
    document.getElementById("nextStep").onclick = () => goTo("role");

    // Go back to Basic Info when "Previous" is clicked from Role Selection
    document.getElementById("prevStep").onclick = () => goTo("basic");

    // When "Next" is clicked on Role tab, fill in confirmation tab with user data
    document.getElementById("nextConfirm").onclick = () => {
        // Populate confirmation summary fields with values from form inputs
        document.getElementById("confirmUsername").textContent = document.getElementById("username").value;
        document.getElementById("confirmFullName").textContent = 
            document.getElementById("firstName").value + " " + document.getElementById("lastName").value;
        document.getElementById("confirmEmail").textContent = document.getElementById("email").value;
        document.getElementById("confirmDepartment").textContent = 
            document.getElementById("department").value || "N/A";
        document.getElementById("confirmRole").textContent = selectedRole.value || "N/A";

        // Move to the Confirmation tab
        goTo("confirmation");
    };

    // Go back to Role Selection tab from Confirmation tab
    document.getElementById("prevConfirm").onclick = () => goTo("role");

   
    // FORM SUBMISSION VALIDATION
   
    // Add custom validation logic on form submission
    form.addEventListener("submit", function (e) {
        // Select all required fields in the form (inputs and selects)
        const requiredFields = form.querySelectorAll("input[required], select[required]");
        let formValid = true;

        // Loop through required fields to validate them
        requiredFields.forEach(field => {
            if (!field.checkValidity()) {
                // If field is invalid, mark it with a red border
                field.classList.add("is-invalid");
                formValid = false;
            } else {
                // Remove red border if field becomes valid
                field.classList.remove("is-invalid");
            }
        });

        // Check if role is selected
        if (!selectedRole.value) {
            alert("Please select a role before submitting.");
            formValid = false;
        }

        // If any field is invalid, prevent form from submitting
        if (!formValid) {
            e.preventDefault();
        }
    });

  
    // REMOVE RED BORDER ON CORRECTION
   
    // As user corrects their input, remove the red "is-invalid" styling
    const allInputs = form.querySelectorAll("input, select");
    allInputs.forEach(input => {
        input.addEventListener("input", () => {
            if (input.checkValidity()) {
                input.classList.remove("is-invalid");
            }
        });
    });
});
