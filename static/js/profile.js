const dialog = document.getElementById("skill-dialog");

document.querySelectorAll(".skill-card").forEach((card) => {
    card.addEventListener("click", () => {
        nameDialog = document.getElementById("dialog-name");
        labelDialog = document.getElementById("dialog-label");
        profDialog = document.getElementById("dialog-proficiency");
        descDialog = document.getElementById("dialog-description");
        imageDialog = document.getElementById("dialog-images");

        nameDialog.textContent = card.dataset.name
        labelDialog.textContent = card.dataset.label
        descDialog.textContent = card.dataset.description
        profDialog.textContent = card.dataset.proficiency
        descDialog.textContent = card.dataset.description
        


    })
})