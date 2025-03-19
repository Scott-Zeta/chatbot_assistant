import openai
from flask import session

class ThreadService:
    def __init__(self):
        self.client = openai
        self.thread = None
        
    def ensure_thread(self):
        """Ensures thread exists for the current session"""
        if self.thread is None:
            self.thread = self.get_or_create_thread()
            
    def get_or_create_thread(self):
        """Retrieves existing thread or creates new one"""
        if 'thread_id' in session:
            try:
                self.thread = self.client.beta.threads.retrieve(
                    thread_id=session['thread_id']
                )
                return self.thread
            except Exception:
                return self._create_new_thread()
        return self._create_new_thread()
    
    def _create_new_thread(self):
        """Creates a new thread and stores ID in session"""
        thread = self.client.beta.threads.create()
        session['thread_id'] = thread.id
        self.thread = thread
        return thread
    
    def add_message(self, content: str, role: str = "user"):
        """Adds a message to the thread"""
        self.ensure_thread()
        try:
            return self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role=role,
                content=content
            )
        except Exception as e:
            raise RuntimeError(f"Failed to add message: {str(e)}")
    
    def get_message_history(self):
        """Retrieves message history from thread"""
        self.ensure_thread()
        try:
            messages = self.client.beta.threads.messages.list(self.thread.id)
            return [
                {
                    "role": msg.role,
                    "content": msg.content[0].text.value
                }
                for msg in messages.data
            ]
        except Exception as e:
            raise RuntimeError(f"Failed to get message history: {str(e)}")
        