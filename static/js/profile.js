const dialog = document.getElementById("skill-dialog");

document.querySelectorAll(".skill-card").forEach((card) => {
    card.addEventListener("click", () => {
        const skillDialog = document.getElementById("skill-dialog")

        const nameDialog = document.getElementById("dialog-name");
        const labelDialog = document.getElementById("dialog-label");
        const profDialog = document.getElementById("dialog-proficiency");
        const descDialog = document.getElementById("dialog-description");
        const imageDialog = document.getElementById("dialog-images");

        nameDialog.textContent = card.dataset.name
        labelDialog.textContent = card.dataset.label
        descDialog.textContent = card.dataset.description
        profDialog.textContent = card.dataset.proficiency
        descDialog.textContent = card.dataset.description
        
        skillDialog.showModal()

        
    })
})