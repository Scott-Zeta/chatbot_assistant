from assistant_module import Assistant
from dotenv import load_dotenv
from thread_module import Thread

load_dotenv()

if __name__ == '__main__':
    assistant = Assistant()
    
    thread = Thread()
    thread.create_retrieve_thread()