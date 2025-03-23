// Constants
const DOM_ELEMENTS = {
  chatBody: document.querySelector('.chat-body'),
  messageInput: document.querySelector('.message-input'),
  sendMessageButton: document.querySelector('#send-message'),
  chatbotToggler: document.querySelector('#chatbot-toggler'),
  closeChatbot: document.querySelector('#close-chatbot'),
  promptButtons: document.querySelectorAll('.prompt-group .prompt'),
};

const CONFIG = {
  BASE_URL: 'http://127.0.0.1:5000',
  API_URL: '/assist',
  HISTORY_API_URL: '/history',
  THINKING_DELAY: 600,
};

const TEMPLATE = {
  BOT_AVATAR_SVG: `<svg class="bot-avatar" xmlns="http://www.w3.org/2000/svg" width="50" height="50" viewBox="0 0 1024 1024">
    <path d="M738.3 287.6H285.7c-59 0-106.8 47.8-106.8 106.8v303.1c0 59 47.8 106.8 106.8 106.8h81.5v111.1c0 .7.8 1.1 1.4.7l166.9-110.6 41.8-.8h117.4l43.6-.4c59 0 106.8-47.8 106.8-106.8V394.5c0-59-47.8-106.9-106.8-106.9zM351.7 448.2c0-29.5 23.9-53.5 53.5-53.5s53.5 23.9 53.5 53.5-23.9 53.5-53.5 53.5-53.5-23.9-53.5-53.5zm157.9 267.1c-67.8 0-123.8-47.5-132.3-109h264.6c-8.6 61.5-64.5 109-132.3 109zm110-213.7c-29.5 0-53.5-23.9-53.5-53.5s23.9-53.5 53.5-53.5 53.5 23.9 53.5 53.5-23.9 53.5-53.5 53.5zM867.2 644.5V453.1h26.5c19.4 0 35.1 15.7 35.1 35.1v121.1c0 19.4-15.7 35.1-35.1 35.1h-26.5zM95.2 609.4V488.2c0-19.4 15.7-35.1 35.1-35.1h26.5v191.3h-26.5c-19.4 0-35.1-15.7-35.1-35.1zM561.5 149.6c0 23.4-15.6 43.3-36.9 49.7v44.9h-30v-44.9c-21.4-6.5-36.9-26.3-36.9-49.7 0-28.6 23.3-51.9 51.9-51.9s51.9 23.3 51.9 51.9z"/>
  </svg>`,
};

const ndisFAQs = [
  {
    id: 1,
    topic: 'Introduction to the NDIS',
    questions: [
      'What is the NDIS, and how does it work?',
      'Who is eligible for the NDIS?',
      'How do I apply for the NDIS?',
      'What types of support does the NDIS cover?',
      'What is the difference between the NDIS and other government disability services?',
    ],
  },
  {
    id: 2,
    topic: 'Eligibility & Application',
    questions: [
      'How do I know if I meet the NDIS eligibility criteria?',
      'What documents do I need to provide for my application?',
      'How long does it take to get approved for the NDIS?',
      'What happens if my application is rejected?',
      'Can I appeal an NDIS decision if I am found ineligible?',
    ],
  },
  {
    id: 3,
    topic: 'NDIS Plans & Funding',
    questions: [
      'How is my NDIS funding determined?',
      'What is the difference between Core, Capacity Building, and Capital Supports?',
      'How can I use my NDIS funds?',
      'Can I change my NDIS plan if my needs change?',
      'What is a plan review, and how do I request one?',
    ],
  },
  {
    id: 4,
    topic: 'NDIS Support & Services',
    questions: [
      'What kinds of services and supports can I access through the NDIS?',
      'Can the NDIS help with housing or home modifications?',
      'Does the NDIS cover assistive technology, such as wheelchairs or communication devices?',
      'How do I find and choose NDIS service providers?',
      'Can I use NDIS funding for therapy and counseling?',
    ],
  },
  {
    id: 5,
    topic: 'Managing an NDIS Plan',
    questions: [
      'What are the different types of NDIS plan management (self-managed, plan-managed, NDIA-managed)?',
      'How do I track my NDIS funding and spending?',
      'Can I switch from NDIA-managed to self-managed or plan-managed?',
      'What happens if I run out of NDIS funds before my plan ends?',
      'Can I hire my own support workers with NDIS funding?',
    ],
  },
  {
    id: 6,
    topic: 'Other NDIS-Related Topics',
    questions: [
      'How does the NDIS work with Medicare and private health insurance?',
      'Can I use NDIS funding for travel and transport?',
      'What happens to my NDIS plan if I move interstate?',
      'What should I do if I have a complaint about my NDIS plan or provider?',
      'How does the NDIS support people with psychosocial disabilities?',
    ],
  },
];

class ChatBot {
  constructor() {
    this.messageState = {
      currentMessage: null,
      initialInputHeight: DOM_ELEMENTS.messageInput.scrollHeight,
    };
    this.initializeEventListeners();
    this.loadChatHistory();
  }

  async generateBotResponse(incomingMessageDiv) {
    const messageElement = incomingMessageDiv.querySelector('.message-text');

    try {
      const response = await fetch(`${CONFIG.BASE_URL}${CONFIG.API_URL}`, {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: this.messageState.currentMessage }),
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.error.message);

      messageElement.innerText = data.response.anwser.trim();
      if (
        data.response.follow_up_questions &&
        data.response.follow_up_questions.length > 0
      ) {
        this.createfollowUpQuestions(data.response.follow_up_questions);
      }
    } catch (error) {
      console.error('API Error:', error);
      messageElement.innerText = error.message;
      messageElement.style.color = 'red';
    } finally {
      incomingMessageDiv.classList.remove('thinking');
      this.scrollToBottom();
    }
  }

  createMessageElement(content, ...classes) {
    const div = document.createElement('div');
    div.classList.add('message', ...classes);
    div.innerHTML = content;
    return div;
  }

  createfollowUpQuestions(questions) {
    // append prompt quesiton buttons
    const promptMessageDiv = this.createMessageElement('', 'user-message');
    const promptGroup = document.createElement('div');
    promptGroup.className = 'prompt-group';

    questions.forEach((question) => {
      const button = document.createElement('button');
      button.className = 'prompt';
      button.innerText = question;
      button.addEventListener('click', () => {
        this.messageState.currentMessage = question;
        this.appendUserMessage(question);
        this.showBotResponse().then((incomingMessageDiv) => {
          this.generateBotResponse(incomingMessageDiv);
        });
      });
      promptGroup.appendChild(button);
    });

    promptMessageDiv.appendChild(promptGroup);
    DOM_ELEMENTS.chatBody.appendChild(promptMessageDiv);
  }

  createThinkingIndicator() {
    return `
      <div class="message-text">
        <div class="thinking-indicator">
          ${Array(3).fill('<div class="dot"></div>').join('')}
        </div>
      </div>`;
  }

  handleOutgoingMessage(e) {
    e.preventDefault();
    const messageText = DOM_ELEMENTS.messageInput.value.trim();
    if (!messageText) return;

    this.messageState.currentMessage = messageText;
    this.clearInputField();
    this.appendUserMessage(messageText);
    this.showBotResponse().then((incomingMessageDiv) => {
      this.generateBotResponse(incomingMessageDiv);
    });
  }

  clearInputField() {
    DOM_ELEMENTS.messageInput.value = '';
    DOM_ELEMENTS.messageInput.dispatchEvent(new Event('input'));
  }

  appendUserMessage(text) {
    const messageDiv = this.createMessageElement(
      '<div class="message-text"></div>',
      'user-message'
    );
    messageDiv.querySelector('.message-text').innerText = text;
    DOM_ELEMENTS.chatBody.appendChild(messageDiv);
    this.scrollToBottom();
  }

  showBotResponse() {
    return new Promise((resolve) => {
      setTimeout(() => {
        const botMessageContent = `${
          TEMPLATE.BOT_AVATAR_SVG
        }${this.createThinkingIndicator()}`;
        const incomingMessageDiv = this.createMessageElement(
          botMessageContent,
          'bot-message',
          'thinking'
        );
        DOM_ELEMENTS.chatBody.appendChild(incomingMessageDiv);
        this.scrollToBottom();
        resolve(incomingMessageDiv); // return the message element
      }, CONFIG.THINKING_DELAY);
    });
  }

  async loadChatHistory() {
    try {
      const response = await fetch(
        `${CONFIG.BASE_URL}${CONFIG.HISTORY_API_URL}`,
        {
          credentials: 'include',
        }
      );
      const { history } = await response.json();
      if (!response.ok) throw new Error('Failed to load chat history');

      if (history?.length) {
        history.reverse().forEach((message) => {
          const messageDiv = this.createMessageElement(
            '<div class="message-text"></div>',
            message.role === 'user' ? 'user-message' : 'bot-message'
          );
          messageDiv.querySelector('.message-text').innerText = message.content;
          DOM_ELEMENTS.chatBody.appendChild(messageDiv);
        });
        this.scrollToBottom();
      }
    } catch (error) {
      console.error('History Error:', error);
    }
  }

  scrollToBottom() {
    DOM_ELEMENTS.chatBody.scrollTo({
      top: DOM_ELEMENTS.chatBody.scrollHeight,
      behavior: 'smooth',
    });
  }

  initializeEventListeners() {
    // Message input handlers
    DOM_ELEMENTS.messageInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && e.target.value.trim()) {
        this.handleOutgoingMessage(e);
      }
    });

    DOM_ELEMENTS.messageInput.addEventListener('input', (e) => {
      e.target.style.height = `${this.messageState.initialInputHeight}px`;
      e.target.style.height = `${e.target.scrollHeight}px`;
    });

    // Button click handlers
    DOM_ELEMENTS.sendMessageButton.addEventListener('click', (e) =>
      this.handleOutgoingMessage(e)
    );

    DOM_ELEMENTS.chatbotToggler.addEventListener('click', () =>
      document.body.classList.toggle('show-chatbot')
    );

    DOM_ELEMENTS.closeChatbot.addEventListener('click', () =>
      document.body.classList.remove('show-chatbot')
    );

    // Prompt button handlers
    DOM_ELEMENTS.promptButtons.forEach((button) => {
      button.addEventListener('click', () => {
        this.messageState.currentMessage = button.innerText.trim();
        this.appendUserMessage(this.messageState.currentMessage);
        this.showBotResponse().then((incomingMessageDiv) => {
          this.generateBotResponse(incomingMessageDiv);
        });
      });
    });
  }
}

// Initialize chatbot
const chatbot = new ChatBot();
