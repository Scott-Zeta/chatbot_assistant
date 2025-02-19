# Chatbot Assistant

## Overview

The Chatbot Assistant is a web-based application that uses OpenAI’s Assistant API to provide responsive, intelligent conversations. The application is built with the Flask framework for managing server-side logic and uses standard web technologies (HTML, CSS, and JavaScript) for its user interface. This setup ensures the chatbot is both powerful and easy to interact with.

## Features

1. **Conversational Interaction**:  
   Engage in basic, natural-sounding chats. Simply type your question, and the chatbot will respond in real time.

2. **User-Specific Conversations**:  
   Each user’s conversation is tracked using Flask sessions. This means multiple users can chat with the bot at the same time, and each person’s chat history remains separate and private.

3. **File-Based Knowledge Retrieval**:  
   Upload files to a vector database and the chatbot can search for information within those files to provide more accurate, context-specific answers.

4. **Function Calling (e.g. Weather Information)**:  
   The chatbot can call external functions based on your requests. For example, it can fetch current weather data for any city as a demonstration of this functionality.

5. **Flexible Integration Options**:  
   Use the standalone user interface or integrate the chatbot into your own website via the provided widget JavaScript file.

## Requirements

1. **OpenAI API Access**:  
   You will need a valid OpenAI API key with sufficient credit to support the Assistant’s functionality.

2. **Optional Weather API Access**:  
   To enable the weather fetching feature, you will need a free current weather API key from [Weatherbit](https://www.weatherbit.io/api).

## Running the Application

1. **Create or Configure Your Assistant**:  
   You can run `./initial/assistant_manager.py` to create an Assistant, but it is often easier to use the [OpenAI Dashboard](https://platform.openai.com/assistants) to manage your assistants. This reduces the risk of creating multiple duplicate assistants.

2. **Set Your Assistant ID**:  
   Copy the Assistant ID from the OpenAI dashboard and paste it into the `.env` file as `ASSISTANT_ID=`.

3. **Start the Application**:  
   Run `./app.py` to start the server.

4. **Access the User Interface**:  
   Open a web browser and go to `http://localhost:5000`. You will see the chatbot’s graphical interface, ready for interaction.

5. **Embed the Widget**:  
   To integrate the chatbot into another website, add the following script tag to your site’s HTML:
   ```html
   <script src="http://localhost:5000/static/js/widget.js" defer></script>
   ```
   This allows you to include the chatbot widget seamlessly.
