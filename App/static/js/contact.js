// Function to save form data to local storage
function saveFormData() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;
    
    // Save form data in local storage
    localStorage.setItem('contactForm_name', name);
    localStorage.setItem('contactForm_email', email);
    localStorage.setItem('contactForm_message', message);
  }
  
  // Function to load form data from local storage
  function loadFormData() {
    const name = localStorage.getItem('contactForm_name');
    const email = localStorage.getItem('contactForm_email');
    const message = localStorage.getItem('contactForm_message');
    
    // Set form fields if data exists in local storage
    if (name) document.getElementById('name').value = name;
    if (email) document.getElementById('email').value = email;
    if (message) document.getElementById('message').value = message;
  }
  
  // Function to clear form data from local storage
  function clearFormData() {
    localStorage.removeItem('contactForm_name');
    localStorage.removeItem('contactForm_email');
    localStorage.removeItem('contactForm_message');
  }
  
  // Updated validation function that also clears storage on successful submission
  function validateContactForm() {
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const message = document.getElementById('message').value.trim();
    
    if (!name || !email || !message) {
      alert("All fields are required.");
      return false;
    }
    
    document.getElementById("formResult").innerText = "Thank you for contacting us!";
    
    // Clear the form data from local storage after successful submission
    clearFormData();
    
    // Reset the form
    document.getElementById('name').value = '';
    document.getElementById('email').value = '';
    document.getElementById('message').value = '';
    
    return false;
  }
  
  // Add event listeners to form fields to save data as the user types
  function setupFormListeners() {
    const formFields = ['name', 'email', 'message'];
    
    formFields.forEach(field => {
      const element = document.getElementById(field);
      element.addEventListener('input', saveFormData);
    });
  }
  
  // Run when the page loads
  document.addEventListener('DOMContentLoaded', function() {
    // Load any saved form data
    loadFormData();
    
    // Set up the event listeners
    setupFormListeners();
  });