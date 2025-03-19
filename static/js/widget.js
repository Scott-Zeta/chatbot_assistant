(function () {
  // Set the base URL dynamically
  const BASE_URL = 'http://127.0.0.1:5000'; // Use HTTP unless SSL is configured

  // Create chatbot container
  const chatbotContainer = document.createElement('div');
  chatbotContainer.id = 'my-chatbot-container';

  // Fetch and insert chatbot widget HTML
  fetch(`${BASE_URL}/static/html/chatbot-widget.html`)
    .then((response) => response.text())
    .then((html) => {
      chatbotContainer.innerHTML = html;
      chatbotContainer.style.zIndex = '9999';
      chatbotContainer.style.position = 'fixed';
      document.body.appendChild(chatbotContainer);

      // Load CSS dynamically
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = `${BASE_URL}/static/css/style.css`;
      document.head.appendChild(link);

      // Load chatbot logic only after widget is loaded
      const script = document.createElement('script');
      script.src = `${BASE_URL}/static/js/script.js`;
      script.defer = true;
      document.body.appendChild(script);
    })
    .catch((error) => console.error('Error loading chatbot widget:', error));
})();
