import json
import time
from typing import List
import openai
from pydantic import BaseModel
from app.functions.weather_utils import get_weather

class NDISResponseModel(BaseModel):
    anwser: str
    """The response to the user's inquiry about NDIS."""

    follow_up_questions: List[str]
    """Relevant follow-up questions to guide the user's exploration."""


class RunService:
    def __init__(self, thread_service):
        self.client = openai
        self.thread_service = thread_service
        
    def create_run(self, assistant_id: str, max_retries: int = 5):
        """Creates and manages a run with the assistant"""
        try:
            run = self._create_and_handle_run(assistant_id, max_retries)
            response = self._process_run_response(run)
            return json.loads(response)
        except Exception as e:
            raise RuntimeError(f"Failed to run assistant: {str(e)}")
    
    def _create_and_handle_run(self, assistant_id: str, max_retries: int):
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=self.thread_service.thread.id,
            assistant_id=assistant_id,
            response_format={'type': 'json_schema',
           'json_schema': 
              {
                "name":"whocares", 
                "schema": NDISResponseModel.model_json_schema()
              }}
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
            thread_id=self.thread_service.thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
    
    def _process_run_response(self, run):
        messages = self.client.beta.threads.messages.list(
            thread_id=self.thread_service.thread.id
        )
        return messages.data[0].content[0].text.value