document.addEventListener("DOMContentLoaded", function () {
  const dobInput = document.getElementById("dob");
  const parentEmailContainer = document.getElementById("parent-email-container");
  const parentEmailInput = document.getElementById("parent_email");
  const roleSelect = document.getElementById("role");

  function calculateAge(dobValue) {
    const dob = new Date(dobValue);
    const today = new Date();
    let age = today.getFullYear() - dob.getFullYear();
    const m = today.getMonth() - dob.getMonth();
    if (m < 0 || (m === 0 && today.getDate() < dob.getDate())) {
      age--;
    }
    return age;
  }

  function toggleParentEmail() {
    const role = roleSelect.value;
    const dobValue = dobInput.value;

    if (!dobValue) return; // don’t do anything until a date is selected

    const age = calculateAge(dobValue);

    // Only show parent email if role is student & under 18
    if (role === "student" && age < 18) {
      parentEmailContainer.style.display = "block";
      parentEmailInput.required = true;
    } else {
      parentEmailContainer.style.display = "none";
      parentEmailInput.required = false;
      parentEmailInput.value = "";
    }
  }

  // Event listeners
  dobInput.addEventListener("change", toggleParentEmail);
  roleSelect.addEventListener("change", toggleParentEmail);
});

// Password confirmation validation
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("register-form");
  const passwordInput = document.getElementById("password");
  const confirmPasswordInput = document.getElementById("confirm_password");
  const errorContainer = document.getElementById("error-container");

  form.addEventListener("submit", function (event) {
    if (passwordInput.value !== confirmPasswordInput.value) {
      event.preventDefault(); // Prevent form submission
      errorContainer.textContent = "Passwords do not match.";
      errorContainer.style.display = "block";
      confirmPasswordInput.focus();
    } else {
      errorContainer.style.display = "none"; // Clear error if passwords match
    }
  });
});
