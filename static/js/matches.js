document.querySelectorAll(".match-form").forEach(form => {
    form.addEventListener("submit", function() {
        const button = form.querySelector(".match-btn");

        button.textContent = "Matched";
        button.disabled = true;
    });
});