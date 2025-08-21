const chatBox = document.getElementById('chat-box');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');

function appendMessage(sender, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender}`;
    const bubble = document.createElement('div');
    bubble.className = `bubble ${sender}`;
    bubble.textContent = text;
    msgDiv.appendChild(bubble);
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showError(msg) {
    let err = document.getElementById('error-message');
    if (!err) {
        err = document.createElement('div');
        err.id = 'error-message';
        chatBox.parentNode.insertBefore(err, chatBox);
    }
    err.textContent = msg;
}

function clearError() {
    const err = document.getElementById('error-message');
    if (err) err.textContent = '';
}

// Add welcome message when page loads
window.onload = function() {
    appendMessage('bot', 'Hello! I\'m a friendly chatbot. Feel free to talk to me about anything!');
};

chatForm.onsubmit = async function(e) {
    e.preventDefault();
    clearError();
    const message = userInput.value.trim();
    if (!message) return;
    appendMessage('user', message);
    userInput.value = '';
    appendMessage('bot', '...');
    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        const data = await res.json();
        chatBox.removeChild(chatBox.lastChild); // remove '...'
        if (data.response) {
            appendMessage('bot', data.response);
        } else {
            showError(data.error || 'Error from server.');
            appendMessage('bot', '[Error]');
        }
    } catch (e) {
        chatBox.removeChild(chatBox.lastChild);
        showError('Network error.');
        appendMessage('bot', '[Network error]');
    }
};