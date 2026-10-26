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

const reportBtn = document.querySelector(".report-btn")
const reportDialog = document.getElementById("report-dialog")
const closeReport = document.getElementById("close-report")

if (reportBtn) {
reportBtn.addEventListener("click", () => {
    reportDialog.showModal()
})

closeReport.addEventListener("click", () => {
    reportDialog.close()
})
}