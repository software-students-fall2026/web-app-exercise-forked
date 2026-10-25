const socket = io("/dms")
const messageHolder = document.getElementById("messages")
const messageBtn = document.getElementById("message-btn")

function showMessage(text) {
    const div = document.createElement("div")
    div.textContent = text
    messageHolder.appendChild(div)
}

socket.on("connect", () => {
    console.log("Connected")
})

socket.on("receive_dm", (data) => {
    showMessage(`${data.from}: ${data.message}`)
})

socket.on("dm_sent", (data) => {
    showMessage(`You: ${data.message}`)
})

messageBtn.addEventListener("click", () => {
    const to = document.getElementById("recipient").value.trim()
    const message = document.getElementById("message").value.trim()

    if (!to || !message || !socket.connected) {
        return
    }

    socket.emit("send_dm", {
        to: to,
        message: message
    })

    document.getElementById("message").value = ""
})