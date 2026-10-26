const socket = io("/dms")
const messageHolder = document.getElementById("messages")
const messageBtn = document.getElementById("message-btn")

const receiverComponent = document.getElementById("receiver")
const receiverAvatar = receiverComponent.dataset.receiverAvatar
const myAvatar = receiverComponent.dataset.myAvatar

function showMessage(text, avatarUrl) {
    const div = document.createElement("div")
    div.className = "user-row dm-message"

    const img = document.createElement("img")
    img.className = "avatar-small"
    img.src = avatarUrl
    img.alt = ""

    const span = document.createElement("span")
    span.textContent = text

    div.append(img, span)
    messageHolder.appendChild(div)
}

socket.on("connect", () => {
    console.log("Connected")
})

socket.on("receive_dm", (data) => {
    if (data.from_id !== receiverComponent.dataset.user) return
    showMessage(`${data.from_username}: ${data.message}`, receiverAvatar)
})

socket.on("dm_sent", (data) => {
    showMessage(`You: ${data.message}`, myAvatar)
})

messageBtn.addEventListener("click", () => {
    const receiverComponent = document.getElementById('receiver')
    const to = receiverComponent.dataset.user
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