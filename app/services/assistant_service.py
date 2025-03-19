import openai
from config.settings import Config

class AssistantService:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = openai
        self.model = model
        self.assistant = self._initialize_assistant()
        
    def _initialize_assistant(self):
        if not Config.ASSISTANT_ID:
            raise ValueError("Assistant ID not configured in .env file")
        
        try:
            return self.client.beta.assistants.retrieve(
                assistant_id=Config.ASSISTANT_ID
            )
        except Exception as e:
            raise Exception(f"Failed to initialize assistant: {str(e)}")
    
    @property
    def assistant_id(self):
        return self.assistant.id if self.assistant else None