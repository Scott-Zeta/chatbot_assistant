import os
from assistant_module import Assistant
from dotenv import load_dotenv
from thread_module import Thread
from flask import Flask, session

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route('/')
def assist():
    session.permanent = False
    # Create or Retrieve Thread
    thread = Thread()
    thread.retrieve_thread()
    
    #Add Message to Thread
    thread.add_message_to_thread(role="user", content="Hi")
    thread.list_messages()
    
    return f"Current Thread ID: {session.get('thread_id', 'No Thread Found')}"

if __name__ == '__main__':
    assistant = Assistant()

    app.run(debug=True)