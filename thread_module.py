import openai

class Thread:
    
    thread_id = "thread_1LlpHgmuRcp77g8HWwVONCkX"
    
    def __init__(self) -> None:
        self.client = openai
        self.thread = None
        
    def create_retrieve_thread(self):
        if Thread.thread_id:
            self.thread = self.client.beta.threads.retrieve(Thread.thread_id)
            print(self.thread)
        else:
            thread_entity = self.client.beta.threads.create()
            self.thread = thread_entity
            print(self.thread)