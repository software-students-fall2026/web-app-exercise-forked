const passwordInput = document.getElementById("password");
const toggleButton = document.getElementById("toggle-password");
const toggleIcon = document.getElementById("toggle-password-icon")

const eyeOpen = "/static/images/eye.svg";
const eyeClosed = "/static/images/eye-crossed.svg";

toggleButton.addEventListener("click", () => {
    const hidden = passwordInput.type === "password";
    passwordInput.type = hidden ? "text" : "password";
    toggleIcon.src = hidden ? eyeOpen : eyeClosed;
    toggleButton.setAttribute("aria-label", hidden ? "Hide password" : "Show password");
})