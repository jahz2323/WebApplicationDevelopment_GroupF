document.addEventListener("DOMContentLoaded", () => {
    const tabs = Array.from(document.querySelectorAll("#formTabs button"));
    const roleCards = document.querySelectorAll(".role-card");
    const selectedRole = document.getElementById("selectedRole");
    const form = document.getElementById("registrationForm");

    // Highlight selected role visually
    roleCards.forEach(card => {
        card.addEventListener("click", () => {
            roleCards.forEach(c => c.classList.remove("border-primary", "bg-opacity-75", "selected"));
            card.classList.add("border-primary", "bg-opacity-75", "selected");
            selectedRole.value = card.dataset.role;
        });
    });

    // Tab Switching
    function goTo(tabId) {
        tabs.forEach(btn => btn.classList.remove("active"));
        document.querySelector(`[data-bs-target="#${tabId}"]`).classList.add("active");
        document.querySelectorAll(".tab-pane").forEach(tab => tab.classList.remove("show", "active"));
        document.getElementById(tabId).classList.add("show", "active");
    }

    document.getElementById("nextStep").onclick = () => goTo("role");
    document.getElementById("prevStep").onclick = () => goTo("basic");

    document.getElementById("nextConfirm").onclick = () => {
        document.getElementById("confirmUsername").textContent = document.getElementById("username").value;
        document.getElementById("confirmFullName").textContent = document.getElementById("firstName").value + " " + document.getElementById("lastName").value;
        document.getElementById("confirmEmail").textContent = document.getElementById("email").value;
        document.getElementById("confirmDepartment").textContent = document.getElementById("department").value || "N/A";
        document.getElementById("confirmRole").textContent = selectedRole.value || "N/A";

        goTo("confirmation");
    };

    document.getElementById("prevConfirm").onclick = () => goTo("role");

    // Custom validation on submit
    form.addEventListener("submit", function (e) {
        const requiredFields = form.querySelectorAll("input[required], select[required]");
        let formValid = true;

        requiredFields.forEach(field => {
            if (!field.checkValidity()) {
                field.classList.add("is-invalid");
                formValid = false;
            } else {
                field.classList.remove("is-invalid");
            }
        });

        if (!selectedRole.value) {
            alert("Please select a role before submitting.");
            formValid = false;
        }

        if (!formValid) {
            e.preventDefault();
        }
    });

    // Remove red border on input correction
    const allInputs = form.querySelectorAll("input, select");
    allInputs.forEach(input => {
        input.addEventListener("input", () => {
            if (input.checkValidity()) {
                input.classList.remove("is-invalid");
            }
        });
    });
});
