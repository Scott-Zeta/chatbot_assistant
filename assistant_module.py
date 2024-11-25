import openai

class Assistant:
    
    def __init__(self, model: str = "gpt-4o-mini") -> None:
        self.client = openai
        self.model = model
        self.assistant = None
        
        self.create_assistant(name="NDIS Assistant",
                              instructions="You are an assistant for the National Disability Insurance Scheme (NDIS). You are helping a participant understand the NDIS plan and how to use it.",
                              model = self.model,
                              temperature = 0.2,
                              tools=[{"type": "file_search"}],
                              )
            
    def create_assistant(self, name, instructions, model, tools, temperature):
        assistant_entity = self.client.beta.assistants.create(name=name, instructions=instructions, tools=tools, model=model, temperature=temperature)
        self.assistant = assistant_entity