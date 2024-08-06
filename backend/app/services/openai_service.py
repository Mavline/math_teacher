from openai import OpenAI
from app.config import settings
from typing import List, Optional
import time

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class OpenAIService:
    @staticmethod
    def create_assistant(name: str):
        instructions = """
        You are a friendly and patient math teacher and tutor for students aged 8-11.
        Your goal is to explain math concepts in a simple and engaging way, as if talking to a child.
        Use everyday examples and simple language.
        If the student doesn't understand, try explaining differently using analogies or visual descriptions.
        Ask questions to ensure the student is following your explanation.
        Always be encouraging and supportive.
        Break down complex ideas into small, easy-to-understand parts.
        If you need to use math terms, always explain what they mean.
        Remember, you're replacing a real teacher, so your explanations should be very clear and accessible.
        Respond in the same language as the student's question.
        """

        assistant = client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model="gpt-4o-mini",
            tools=[{"type": "code_interpreter"}, {"type": "file_search"}]
        )
        return {
            "id": assistant.id,
            "name": assistant.name,
            "instructions": assistant.instructions,
            "model": assistant.model,
            "tools": assistant.tools
        }

    @staticmethod
    def create_thread():
        return client.beta.threads.create()

    @staticmethod
    def add_message_to_thread(thread_id: str, content: str, attachments: Optional[List[dict]] = None):
        message_params = {
            "thread_id": thread_id,
            "role": "user",
            "content": content
        }
        if attachments:
            message_params["file_ids"] = [attachment["file_id"] for attachment in attachments]
        
        return client.beta.threads.messages.create(**message_params)

    @staticmethod
    def run_assistant(thread_id: str, assistant_id: str):
        return client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

    @staticmethod
    def wait_for_run_completion(thread_id: str, run_id: str):
        while True:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.status == 'completed':
                return run
            elif run.status in ['failed', 'cancelled', 'expired']:
                raise Exception(f"Run ended with status: {run.status}")
            time.sleep(1)

    @staticmethod
    def get_messages(thread_id: str):
        return client.beta.threads.messages.list(thread_id=thread_id)

    @staticmethod
    def upload_file(file_path: str):
        with open(file_path, "rb") as file:
            return client.files.create(file=file, purpose="assistants")

    @staticmethod
    def chat(thread_id: str, assistant_id: str, message: str, attachments: Optional[List[dict]] = None):
        OpenAIService.add_message_to_thread(thread_id, message, attachments)
        run = OpenAIService.run_assistant(thread_id, assistant_id)
        OpenAIService.wait_for_run_completion(thread_id, run.id)
        messages = OpenAIService.get_messages(thread_id)
        return messages.data[0].content[0].text.value
