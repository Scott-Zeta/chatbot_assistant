import os
from assistant_module import Assistant
from dotenv import load_dotenv
from thread_module import Thread
from flask import Flask, session, request, jsonify,render_template
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
cors = CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

app.config.update(
  SESSION_COOKIE_SAMESITE="None",
  SESSION_COOKIE_SECURE=True
)

@app.route('/')
def chat_widget():
    return render_template('bot_widget.html')

@app.route('/assist', methods=["POST"])
def assist():
    query = request.json.get('query')
    
    session.permanent = False
    # Create or Retrieve Thread
    thread = Thread()
    thread.retrieve_thread()
    
    #Add Message to Thread
    thread.add_message_to_thread(role="user", content=f"{query}")
    
    # Run Assistant
    response = thread.run_assistant(assistant_id=Assistant.assistant_id,instruction="")
    
    return jsonify({'response': response})

@app.route('/history', methods=["GET"])
def history():
    session.permanent = False
    # Create or Retrieve Thread
    thread = Thread()
    thread.retrieve_thread()
    # Retrieve Messages History
    history = thread.list_messages()
    return jsonify({'history': history})

if __name__ == '__main__':
    assistant = Assistant()

    app.run(debug=True)