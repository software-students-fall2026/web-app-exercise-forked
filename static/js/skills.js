document.querySelectorAll(".skills-list").forEach((div) => {
    const field = div.dataset.field
    const input = div.querySelector("[data-entry]")
    const addButton = div.querySelector("[data-add]")
    const list = div.querySelector("[data-list]")

    function addSkill() {
        const value = input.value.trim()
        if (!value) {
            return
        }

        const item = document.createElement("div")
        item.className = "skills-list-item"

        const text = document.createElement("span")
        text.textContent = value

        // this field is hidden and sent to flask
        const flaskInput = document.createElement("input")
        flaskInput.type = "hidden"
        flaskInput.name = field
        flaskInput.value = value

        const removeButton = document.createElement("button")
        removeButton.type = "button"
        removeButton.textContent = "Remove"

        removeButton.addEventListener("click", () => {
            item.remove()
        })

        item.append(text, flaskInput, removeButton)
        list.append(item)

        input.value = ""
        input.focus()
    }

    addButton.addEventListener("click", addSkill)

    input.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
            event.preventDefault()
            addSkill()
        }
    })
})