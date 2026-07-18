function sendMessage() {
  const input = document.getElementById('user-input');
  const message = input.value.trim();
  if (!message) return;

  appendMessage('user', message);
  input.value = '';

  fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message })
  })
    .then(res => res.json())
    .then(data => {
      appendMessage('bot', data.reply);
    })
    .catch((err) => {
      console.error("Fetch error:", err);
      appendMessage('bot', "Sorry, I couldn't reach the server.");
    });
}

function appendMessage(sender, message) {
  const chatWindow = document.getElementById('chat-window');
  const messageDiv = document.createElement('div');
  messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
  messageDiv.textContent = message;
  chatWindow.appendChild(messageDiv);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

document.getElementById("user-input").addEventListener("keydown", function (event) {
  if (event.key === "Enter") {
    event.preventDefault();
    sendMessage();
  }
});

function exportChat() {
  const chatWindow = document.getElementById("chat-window");
  const messages = chatWindow.querySelectorAll(".user-message, .bot-message");

  let textContent = "";
  messages.forEach(msg => {
    const prefix = msg.classList.contains("user-message") ? "You: " : "Bot: ";
    textContent += prefix + msg.textContent + "\n";
  });

  const blob = new Blob([textContent], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "chat.txt";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
