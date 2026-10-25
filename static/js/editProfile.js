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

document.querySelectorAll(".add-row").forEach((button) => {
    button.addEventListener("click", () => {
        const rows = button.previousElementSibling
        const newRow = rows.lastElementChild.cloneNode(true)
        clearRow(newRow)
        rows.append(newRow)
    })
})

document.addEventListener("click", (event) => {
    if (!event.target.matches(".remove-skill")) {
        return
    }
    const row = event.target.closest(".skill-row")
    if (row.parentElement.children.length > 1) {
        row.remove()
    } else {
        clearRow(row)
    }
})

function clearRow(row) {
    row.querySelectorAll("input, textarea").forEach((field) => field.value = "")
    row.querySelector("select").selectedIndex = 0
}

const avatar = document.getElementById("avatar")
const avatarImg = document.getElementById("avatarImg")
avatar.addEventListener("change", () => {
    avatarImg.src = avatar.value
})