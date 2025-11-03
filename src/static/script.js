class TrumpChatbot {
    constructor() {
        this.conversation = [];
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.displayInitialMessage();
    }
    
    setupEventListeners() {
        // Send message
        document.getElementById('sendButton').addEventListener('click', () => this.handleSendMessage());
        document.getElementById('messageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleSendMessage();
            }
        });
        
        // Settings modal
        document.getElementById('settingsBtn').addEventListener('click', () => this.showSettingsModal());
        document.getElementById('closeSettings').addEventListener('click', () => this.hideSettingsModal());
        
        // Close modal when clicking outside
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                e.target.style.display = 'none';
            }
        });
    }
    
    showSettingsModal() {
        document.getElementById('settingsModal').style.display = 'block';
    }
    
    hideSettingsModal() {
        document.getElementById('settingsModal').style.display = 'none';
    }
    
    displayInitialMessage() {
        const initialMessage = "Look, let me tell you — I'm here, and frankly, nobody does this better than me. Nobody! I've done incredible things, tremendous things, and people know it. The fake news won't tell you, but the people — they get it. They really do. So what's on your mind? Let's talk. We're going to make this conversation great, believe me!";
        document.getElementById('initialMessage').textContent = initialMessage;
    }
    
    handleSendMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message to chat
        this.addMessageToChat(message, 'user');
        
        // Add to conversation history
        this.conversation.push({
            role: 'user',
            content: message
        });
        
        // Clear input
        input.value = '';
        
        // Show typing indicator
        this.showTypingIndicator();
        
        // Send to backend
        this.sendMessageToBackend(message);
    }
    
    addMessageToChat(message, sender) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const messageSpan = document.createElement('span');
        messageSpan.textContent = message;
        messageDiv.appendChild(messageSpan);
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    showTypingIndicator() {
        const chatMessages = document.getElementById('chatMessages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message trump-message typing-indicator';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = '<span>Trump is typing...</span>';
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    async sendMessageToBackend(message) {
        try {
            const response = await fetch('/api/chatbot/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message
                })
            });
            
            const data = await response.json();
            
            this.removeTypingIndicator();
            
            if (data.success) {
                // Add Trump's response to chat
                this.addMessageToChat(data.response, 'trump');
                
                // Add to conversation history
                this.conversation.push({
                    role: 'assistant',
                    content: data.response
                });
            } else {
                this.addMessageToChat('Error: ' + data.message, 'trump');
            }
        } catch (error) {
            console.error('Error:', error);
            this.removeTypingIndicator();
            this.addMessageToChat('Sorry, there was an error communicating with the server.', 'trump');
        }
    }
}

// Initialize the chatbot when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new TrumpChatbot();
});
