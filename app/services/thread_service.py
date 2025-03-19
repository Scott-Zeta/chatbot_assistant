import openai
import json
import time
from flask import session
from app.utils.weather_utils import get_weather

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
    
    def run_assistant(self, assistant_id: str, instruction: str = "", max_retries: int = 10):
        """Runs the assistant on the current thread"""
        self.ensure_thread()
        try:
            run = self._create_and_handle_run(assistant_id, max_retries)
            return self._process_run_response(run)
        except Exception as e:
            raise RuntimeError(f"Failed to run assistant: {str(e)}")
    
    def _create_and_handle_run(self, assistant_id: str, max_retries: int):
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id,
            assistant_id=assistant_id
        )
        
        retry_count = 0
        while retry_count < max_retries:
            if run.status == 'completed':
                return run
            elif run.status == 'requires_action':
                run = self._handle_required_actions(run)
            elif run.status == 'failed':
                retry_count += 1
            else:
                time.sleep(2)
        
        raise RuntimeError("Maximum retries exceeded")
    
    def _handle_required_actions(self, run):
        tool_outputs = []
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            arguments = json.loads(tool.function.arguments)
            if tool.function.name == "get_weather":
                output = get_weather(city=arguments['city'])
                tool_outputs.append({
                    "tool_call_id": tool.id,
                    "output": output
                })
            else:
                raise ValueError(f"Unknown function: {tool.function.name}")
                
        return self.client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=self.thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
    
    def _process_run_response(self, run):
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread.id
        )
        return messages.data[0].content[0].text.value