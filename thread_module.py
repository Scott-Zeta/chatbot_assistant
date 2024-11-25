import openai
from flask import session

class Thread:
    
    def __init__(self) -> None:
        self.client = openai
        self.thread = None
        
    def retrieve_thread(self):
        if 'thread_id' in session:
            try:
                self.thread = self.client.beta.threads.retrieve(session['thread_id'])
                print(f"Thread Retrieved: {self.thread}")
            except Exception as e:
                print(f"Session didn't found: {e}")
                self.create_new_thread()
        else:
            self.create_new_thread()
            
    def create_new_thread(self):
        thread_entity = self.client.beta.threads.create()
        session['thread_id'] = thread_entity.id
        self.thread = thread_entity
        print(f"New Thread Created: {self.thread}")