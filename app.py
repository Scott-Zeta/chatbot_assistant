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
    thread = Thread()
    thread.create_retrieve_thread()
    return f"Current Thread ID: {session.get('thread_id', 'No Thread Found')}"

if __name__ == '__main__':
    assistant = Assistant()

    app.run(debug=False)