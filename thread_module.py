import openai
import time
import json
from flask import session
from functions.functions import get_weather

class Thread:
    
    def __init__(self) -> None:
        self.client = openai
        self.thread = None
        
    def retrieve_thread(self):
        if 'thread_id' in session:
            try:
                self.thread = self.client.beta.threads.retrieve(thread_id=session['thread_id'])
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
    
    def add_message_to_thread(self, role, content):
        if self.thread:
            try:
                message = self.client.beta.threads.messages.create(thread_id=self.thread.id, role=role, content=content)
                # print(f"Message Added: {message}")
            except Exception as e:
                print(f"Add Message Failed: {e}")
    
    # Helper function for validation        
    def list_messages(self):
        messages = self.client.beta.threads.messages.list(self.thread.id)
        history = []
        for message in messages:
            message_dic = {
                "role": message.role,
                "content": message.content[0].text.value
            }
            history.append(message_dic)
        return history
                
    def run_assistant(self,assistant_id, instruction):
        if self.thread:
            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=self.thread.id,
                assistant_id=assistant_id,
                )
            while True:
                if run.status == 'completed':
                    messages = self.client.beta.threads.messages.list(
                        thread_id=self.thread.id
                    )
                    summary = []

                    last_message = messages.data[0]
                    # print(f"last_message: {last_message}")
                    response = last_message.content[0].text.value
                    summary.append(response)

                    return "\n".join(summary)
                elif run.status == 'requires_action':
                    print("Action Required")
                    tool_outputs = [] # Output from tools
                    
                    for tool in run.required_action.submit_tool_outputs.tool_calls: # iterate over all tools has been called
                        arguments = json.loads(tool.function.arguments) # arguments array for tools
                        if tool.function.name == "get_weather":
                            output = get_weather(city=arguments['city'])
                            print(f"Output Data: {output}")
                            tool_outputs.append({"tool_call_id": tool.id, "output": output}) # append output from function to tool_outputs
                        else:
                            raise ValueError(f"Unknown function: {tool.function.name}")
                    
                    if tool_outputs:
                        try: 
                            run = self.client.beta.threads.runs.submit_tool_outputs_and_poll(
                                thread_id=self.thread.id,
                                run_id=run.id,
                                tool_outputs=tool_outputs
                            ) # Submit tool outputs and poll the run result
                            print(f"Tool Outputs Submitted")
                        except Exception as e:
                            print(f"Submit Tool Outputs Failed: {e}")
                    else:
                        print("No outputs to submit")
                else:
                    print(run.status)
                time.sleep(2)