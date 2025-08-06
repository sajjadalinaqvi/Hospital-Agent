// Global variables
let isListening = false;
let isMuted = false;
let currentChatId = null;
let chatHistory = [];
let mediaRecorder = null;
let audioChunks = [];

// DOM elements
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.getElementById('sidebar');
const newChatBtn = document.getElementById('newChatBtn');
const chatHistoryContainer = document.getElementById('chatHistory');
const voiceToggle = document.getElementById('voiceToggle');
const voiceIcon = document.getElementById('voiceIcon');
const agentStatus = document.getElementById('agentStatus');
const chatMessages = document.getElementById('chatMessages');
const voiceIndicator = document.getElementById('voiceIndicator');
const muteBtn = document.getElementById('muteBtn');
const muteIcon = document.getElementById('muteIcon');
const settingsBtn = document.getElementById('settingsBtn');
const settingsModal = document.getElementById('settingsModal');
const closeSettings = document.getElementById('closeSettings');

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
    initializeChat();
    setupEventListeners();
    startVoiceAssistant();
});

// Theme management
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
    themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
}

// Chat management
function initializeChat() {
    loadChatHistory();
    if (chatHistory.length === 0) {
        createNewChat();
    } else {
        loadChat(chatHistory[0].id);
    }
}

function createNewChat() {
    const chatId = 'chat_' + Date.now();
    const newChat = {
        id: chatId,
        title: 'New Conversation',
        messages: [],
        timestamp: new Date().toISOString()
    };
    
    chatHistory.unshift(newChat);
    saveChatHistory();
    loadChat(chatId);
    renderChatHistory();
}

function loadChat(chatId) {
    currentChatId = chatId;
    const chat = chatHistory.find(c => c.id === chatId);
    
    if (chat) {
        renderMessages(chat.messages);
        updateActiveChatItem(chatId);
    }
}

function addMessage(role, content) {
    const chat = chatHistory.find(c => c.id === currentChatId);
    if (!chat) return;
    
    const message = {
        id: 'msg_' + Date.now(),
        role: role,
        content: content,
        timestamp: new Date().toISOString()
    };
    
    chat.messages.push(message);
    
    // Update chat title if it's the first user message
    if (role === 'user' && chat.messages.length === 1) {
        chat.title = content.substring(0, 30) + (content.length > 30 ? '...' : '');
    }
    
    saveChatHistory();
    renderMessages(chat.messages);
    renderChatHistory();
}

function renderMessages(messages) {
    chatMessages.innerHTML = '';
    
    if (messages.length === 0) {
        renderWelcomeMessage();
        return;
    }
    
    messages.forEach(message => {
        const messageElement = createMessageElement(message);
        chatMessages.appendChild(messageElement);
    });
    
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function renderWelcomeMessage() {
    const welcomeHTML = `
        <div class="welcome-message">
            <div class="message-content">
                <div class="agent-avatar">
                    <i class="fas fa-user-md"></i>
                </div>
                <div class="message-text">
                    <h3>Welcome to Clifton Hospital Voice Assistant</h3>
                    <p>I'm here to help you with:</p>
                    <ul>
                        <li>Booking appointments with doctors</li>
                        <li>Providing guidance for common health issues</li>
                        <li>Answering questions about our hospital services</li>
                        <li>Referring serious cases to appropriate specialists</li>
                    </ul>
                    <p>Start speaking to begin our conversation!</p>
                </div>
            </div>
        </div>
    `;
    chatMessages.innerHTML = welcomeHTML;
}

function createMessageElement(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message-content ${message.role}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'agent-avatar';
    avatar.innerHTML = message.role === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-user-md"></i>';
    
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = message.content;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageText);
    
    return messageDiv;
}

function renderChatHistory() {
    chatHistoryContainer.innerHTML = '';
    
    chatHistory.forEach(chat => {
        const chatItem = document.createElement('div');
        chatItem.className = `chat-item ${chat.id === currentChatId ? 'active' : ''}`;
        chatItem.onclick = () => loadChat(chat.id);
        
        chatItem.innerHTML = `
            <div class="chat-item-title">${chat.title}</div>
            <div class="chat-item-preview">${getLastMessage(chat)}</div>
        `;
        
        chatHistoryContainer.appendChild(chatItem);
    });
}

function getLastMessage(chat) {
    if (chat.messages.length === 0) return 'No messages yet';
    const lastMessage = chat.messages[chat.messages.length - 1];
    return lastMessage.content.substring(0, 50) + (lastMessage.content.length > 50 ? '...' : '');
}

function updateActiveChatItem(chatId) {
    document.querySelectorAll('.chat-item').forEach(item => {
        item.classList.remove('active');
    });
    
    const activeItem = document.querySelector(`.chat-item[onclick*="${chatId}"]`);
    if (activeItem) {
        activeItem.classList.add('active');
    }
}

function saveChatHistory() {
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
}

function loadChatHistory() {
    const saved = localStorage.getItem('chatHistory');
    chatHistory = saved ? JSON.parse(saved) : [];
}

// Voice assistant functionality
function startVoiceAssistant() {
    if (!isListening) {
        isListening = true;
        updateVoiceStatus('listening');
        startContinuousListening();
    }
}

function stopVoiceAssistant() {
    isListening = false;
    updateVoiceStatus('stopped');
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
    }
}

function toggleVoiceAssistant() {
    if (isListening) {
        stopVoiceAssistant();
    } else {
        startVoiceAssistant();
    }
}

function updateVoiceStatus(status) {
    const statusIndicator = document.querySelector('.status-indicator');
    const statusText = agentStatus.querySelector('span:last-child');
    
    switch (status) {
        case 'listening':
            voiceIcon.className = 'fas fa-microphone';
            voiceToggle.classList.add('active');
            statusIndicator.style.background = 'var(--accent-color)';
            statusText.textContent = 'Always listening...';
            voiceIndicator.classList.add('active');
            break;
        case 'processing':
            voiceIcon.className = 'fas fa-spinner fa-spin';
            statusText.textContent = 'Processing...';
            voiceIndicator.classList.remove('active');
            break;
        case 'speaking':
            voiceIcon.className = 'fas fa-volume-up';
            statusText.textContent = 'Speaking...';
            break;
        case 'stopped':
            voiceIcon.className = 'fas fa-microphone-slash';
            voiceToggle.classList.remove('active');
            statusIndicator.style.background = 'var(--secondary-color)';
            statusText.textContent = 'Voice assistant stopped';
            voiceIndicator.classList.remove('active');
            break;
    }
}

async function startContinuousListening() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Start continuous listening loop
        continuousListeningLoop();
        
    } catch (error) {
        console.error('Error accessing microphone:', error);
        updateVoiceStatus('stopped');
        addMessage('assistant', 'Sorry, I cannot access your microphone. Please check your browser permissions.');
    }
}

async function continuousListeningLoop() {
    while (isListening) {
        try {
            const audioBlob = await recordAudio();
            if (audioBlob && audioBlob.size > 0) {
                await processAudio(audioBlob);
            }
        } catch (error) {
            console.error('Error in listening loop:', error);
            await new Promise(resolve => setTimeout(resolve, 1000)); // Wait before retrying
        }
    }
}

function recordAudio() {
    return new Promise(async (resolve) => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };
            
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                stream.getTracks().forEach(track => track.stop());
                resolve(audioBlob);
            };
            
            mediaRecorder.start();
            
            // Stop recording after 5 seconds or when speech ends
            setTimeout(() => {
                if (mediaRecorder && mediaRecorder.state === 'recording') {
                    mediaRecorder.stop();
                }
            }, 5000);
            
        } catch (error) {
            console.error('Error recording audio:', error);
            resolve(null);
        }
    });
}

async function processAudio(audioBlob) {
    updateVoiceStatus('processing');
    
    try {
        const formData = new FormData();
        formData.append('audio', audioBlob, 'audio.wav');
        
        const response = await fetch('/process_voice', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.user_input && data.user_input.trim()) {
            addMessage('user', data.user_input);
            
            if (data.assistant_response) {
                updateVoiceStatus('speaking');
                addMessage('assistant', data.assistant_response);
                
                // Play TTS response if not muted
                if (!isMuted && data.audio_url) {
                    await playAudio(data.audio_url);
                }
            }
        }
        
        updateVoiceStatus('listening');
        
    } catch (error) {
        console.error('Error processing audio:', error);
        updateVoiceStatus('listening');
    }
}

function playAudio(audioUrl) {
    return new Promise((resolve) => {
        const audio = new Audio(audioUrl);
        audio.onended = resolve;
        audio.onerror = resolve;
        audio.play();
    });
}

function toggleMute() {
    isMuted = !isMuted;
    muteIcon.className = isMuted ? 'fas fa-volume-mute' : 'fas fa-volume-up';
    muteBtn.title = isMuted ? 'Unmute' : 'Mute';
}

// Event listeners
function setupEventListeners() {
    themeToggle.addEventListener('click', toggleTheme);
    
    sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
    });
    
    newChatBtn.addEventListener('click', createNewChat);
    voiceToggle.addEventListener('click', toggleVoiceAssistant);
    muteBtn.addEventListener('click', toggleMute);
    
    settingsBtn.addEventListener('click', () => {
        settingsModal.classList.add('active');
    });
    
    closeSettings.addEventListener('click', () => {
        settingsModal.classList.remove('active');
    });
    
    settingsModal.addEventListener('click', (e) => {
        if (e.target === settingsModal) {
            settingsModal.classList.remove('active');
        }
    });
    
    // Mobile sidebar toggle
    if (window.innerWidth <= 768) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }
    
    // Handle window resize
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('open');
        }
    });
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey || e.metaKey) {
        switch (e.key) {
            case 'n':
                e.preventDefault();
                createNewChat();
                break;
            case 'm':
                e.preventDefault();
                toggleMute();
                break;
            case 'k':
                e.preventDefault();
                toggleVoiceAssistant();
                break;
        }
    }
});

