function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    const chatMessages = document.getElementById('chatMessages');
    
    // Add user message
    const userDiv = document.createElement('div');
    userDiv.className = 'user-message';
    userDiv.textContent = userInput;
    chatMessages.appendChild(userDiv);
    
    // Clear input
    document.getElementById('userInput').value = '';
    
    // Get response from backend
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        const botDiv = document.createElement('div');
        botDiv.className = 'bot-message';
        botDiv.textContent = data.response;
        chatMessages.appendChild(botDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
        const botDiv = document.createElement('div');
        botDiv.className = 'bot-message';
        botDiv.textContent = 'Sorry, there was an error processing your request.';
        chatMessages.appendChild(botDiv);
    });
}