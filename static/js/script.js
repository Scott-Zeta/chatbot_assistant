const chatBody = document.querySelector('.chat-body');
const messageInput = document.querySelector('.message-input');
const sendMessageButton = document.querySelector('#send-message');
const chatbotToggler = document.querySelector('#chatbot-toggler');
const closeChatbot = document.querySelector('#close-chatbot');
const promptButtons = document.querySelectorAll('.prompt-group .prompt');

const API_URL = `https://chatbot-assistant-h8rm.onrender.com/assist`;
const HISTORY_API_URL = `https://chatbot-assistant-h8rm.onrender.com/history`;

// Store User Input
const userData = {
  message: null,
};

const initialInputHeight = messageInput.scrollHeight;

// Generate bot response using API
const generateBotResponse = async (incomingMessageDiv) => {
  // Select message element to update response
  const messageElement = incomingMessageDiv.querySelector('.message-text');

  // Call Backend API to get response
  const requestOptions = {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: userData.message,
    }),
  };
  try {
    const response = await fetch(API_URL, requestOptions);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error.message);
    const apiResponseText = data.response.trim();

    // Substitute thinking indicator with response text
    messageElement.innerText = apiResponseText;
  } catch (error) {
    console.log(error);
    messageElement.innerText = error.message;
    messageElement.style.color = 'red';
  } finally {
    incomingMessageDiv.classList.remove('thinking');
    chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: 'smooth' });
  }
};

// Create message element with dynamic classes and return it
const createMessageElement = (content, ...classes) => {
  const div = document.createElement('div');
  div.classList.add('message', ...classes);
  div.innerHTML = content;
  return div;
};

// Append and display user messages in chat body
const handleOutgoingMessage = (e) => {
  e.preventDefault();
  userData.message = messageInput.value.trim();
  // Clear input field and reset height
  messageInput.value = '';
  messageInput.dispatchEvent(new Event('input'));
  // messageInput.style.height = `${initialInputHeight}px`;

  //Create user message element
  const messageContent = `<div class="message-text"></div>`;
  const outgoingMessageDiv = createMessageElement(
    messageContent,
    'user-message'
  );
  outgoingMessageDiv.querySelector('.message-text').innerText =
    userData.message;
  chatBody.appendChild(outgoingMessageDiv);
  chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: 'smooth' });

  // Render thinking animation after delay
  setTimeout(() => {
    const messageContent = `<svg
            class="bot-avatar"
            xmlns="http://www.w3.org/2000/svg"
            width="50"
            height="50"
            viewBox="0 0 1024 1024"
          >
            <path
              d="M738.3 287.6H285.7c-59 0-106.8 47.8-106.8 106.8v303.1c0 59 47.8 106.8 106.8 106.8h81.5v111.1c0 .7.8 1.1 1.4.7l166.9-110.6 41.8-.8h117.4l43.6-.4c59 0 106.8-47.8 106.8-106.8V394.5c0-59-47.8-106.9-106.8-106.9zM351.7 448.2c0-29.5 23.9-53.5 53.5-53.5s53.5 23.9 53.5 53.5-23.9 53.5-53.5 53.5-53.5-23.9-53.5-53.5zm157.9 267.1c-67.8 0-123.8-47.5-132.3-109h264.6c-8.6 61.5-64.5 109-132.3 109zm110-213.7c-29.5 0-53.5-23.9-53.5-53.5s23.9-53.5 53.5-53.5 53.5 23.9 53.5 53.5-23.9 53.5-53.5 53.5zM867.2 644.5V453.1h26.5c19.4 0 35.1 15.7 35.1 35.1v121.1c0 19.4-15.7 35.1-35.1 35.1h-26.5zM95.2 609.4V488.2c0-19.4 15.7-35.1 35.1-35.1h26.5v191.3h-26.5c-19.4 0-35.1-15.7-35.1-35.1zM561.5 149.6c0 23.4-15.6 43.3-36.9 49.7v44.9h-30v-44.9c-21.4-6.5-36.9-26.3-36.9-49.7 0-28.6 23.3-51.9 51.9-51.9s51.9 23.3 51.9 51.9z"
            />
          </svg>
          <div class="message-text">
            <div class="thinking-indicator">
              <div class="dot"></div>
              <div class="dot"></div>
              <div class="dot"></div>
            </div>
          </div>`;
    const incomingMessageDiv = createMessageElement(
      messageContent,
      'bot-message',
      'thinking'
    );
    chatBody.appendChild(incomingMessageDiv);
    chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: 'smooth' });
    // Call API to get response and update message element
    generateBotResponse(incomingMessageDiv);
  }, 600);
};

const loadChatHistory = async () => {
  try {
    const response = await fetch(HISTORY_API_URL, { credentials: 'include' });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error.message);

    const { history } = data;
    // Append chat history to chat body
    if (history && history.length) {
      history.reverse();
      history.forEach((message) => {
        const messageContent = `<div class="message-text"></div>`;
        const messageDiv = createMessageElement(
          messageContent,
          message.role === 'user' ? 'user-message' : 'bot-message'
        );
        messageDiv.querySelector('.message-text').innerText = message.content;
        chatBody.appendChild(messageDiv);
      });
      chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: 'smooth' });
    }
  } catch (error) {
    console.error('Error loading chat history:', error.message);
  }
};

// Handle Enter key press for sending messages
messageInput.addEventListener('keydown', (e) => {
  const userMessage = e.target.value.trim();
  if (e.key === 'Enter' && userMessage) {
    handleOutgoingMessage(e);
  }
});

// Auto resize message input field
messageInput.addEventListener('input', (e) => {
  messageInput.style.height = `${initialInputHeight}px`;
  messageInput.style.height = `${messageInput.scrollHeight}px`;
});

// Send message on button click
sendMessageButton.addEventListener('click', (e) => handleOutgoingMessage(e));

// Toggle chatbot visibility
chatbotToggler.addEventListener('click', () => {
  document.body.classList.toggle('show-chatbot');
});
closeChatbot.addEventListener('click', () => {
  document.body.classList.remove('show-chatbot');
});

// Handle prompt button selection
promptButtons.forEach((button) => {
  button.addEventListener('click', (e) => {
    const question = button.innerText.trim();
    userData.message = question;

    const messageContent = `<div class="message-text"></div>`;
    const outgoingMessageDiv = createMessageElement(
      messageContent,
      'user-message'
    );
    outgoingMessageDiv.querySelector('.message-text').innerText =
      userData.message;
    chatBody.appendChild(outgoingMessageDiv);
    chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: 'smooth' });
    // Render thinking animation after delay
    setTimeout(() => {
      const messageContent = `<svg
            class="bot-avatar"
            xmlns="http://www.w3.org/2000/svg"
            width="50"
            height="50"
            viewBox="0 0 1024 1024"
          >
            <path
              d="M738.3 287.6H285.7c-59 0-106.8 47.8-106.8 106.8v303.1c0 59 47.8 106.8 106.8 106.8h81.5v111.1c0 .7.8 1.1 1.4.7l166.9-110.6 41.8-.8h117.4l43.6-.4c59 0 106.8-47.8 106.8-106.8V394.5c0-59-47.8-106.9-106.8-106.9zM351.7 448.2c0-29.5 23.9-53.5 53.5-53.5s53.5 23.9 53.5 53.5-23.9 53.5-53.5 53.5-53.5-23.9-53.5-53.5zm157.9 267.1c-67.8 0-123.8-47.5-132.3-109h264.6c-8.6 61.5-64.5 109-132.3 109zm110-213.7c-29.5 0-53.5-23.9-53.5-53.5s23.9-53.5 53.5-53.5 53.5 23.9 53.5 53.5-23.9 53.5-53.5 53.5zM867.2 644.5V453.1h26.5c19.4 0 35.1 15.7 35.1 35.1v121.1c0 19.4-15.7 35.1-35.1 35.1h-26.5zM95.2 609.4V488.2c0-19.4 15.7-35.1 35.1-35.1h26.5v191.3h-26.5c-19.4 0-35.1-15.7-35.1-35.1zM561.5 149.6c0 23.4-15.6 43.3-36.9 49.7v44.9h-30v-44.9c-21.4-6.5-36.9-26.3-36.9-49.7 0-28.6 23.3-51.9 51.9-51.9s51.9 23.3 51.9 51.9z"
            />
          </svg>
          <div class="message-text">
            <div class="thinking-indicator">
              <div class="dot"></div>
              <div class="dot"></div>
              <div class="dot"></div>
            </div>
          </div>`;
      const incomingMessageDiv = createMessageElement(
        messageContent,
        'bot-message',
        'thinking'
      );
      chatBody.appendChild(incomingMessageDiv);
      chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: 'smooth' });
      // Call API to get response and update message element
      generateBotResponse(incomingMessageDiv);
    }, 600);
  });
});

loadChatHistory();
