import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai

def create_assistant(name, instructions, model, tools, temperature):
        assistant_entity = client.beta.assistants.create(name=name, instructions=instructions, tools=tools, model=model, temperature=temperature)
        
create_assistant(name="Test Assistant",
                                instructions="You are an assistant for the National Disability Insurance Scheme (NDIS). You are helping a participant understand the NDIS plan and how to use it.",
                                model = "gpt-4o-mini",
                                temperature = 0.2,
                                tools=[{"type": "file_search"}],
                                )