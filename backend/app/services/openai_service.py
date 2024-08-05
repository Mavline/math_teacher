from openai import OpenAI
from app.config import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)


class OpenAIService:
    @staticmethod
    def create_assistant(name: str, instructions: str):
        assistant = client.beta.assistants.create(
            name=name,
            instructions=instructions,
            tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
            model="gpt-4o-mini"
        )
        return assistant

    @staticmethod
    def create_thread():
        thread = client.beta.threads.create()
        return thread

    @staticmethod
    def add_message_to_thread(thread_id: str, content: str):
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=content
        )
        return message

    @staticmethod
    def run_assistant(thread_id: str, assistant_id: str):
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        return run

    @staticmethod
    def get_run_status(thread_id: str, run_id: str):
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        return run

    @staticmethod
    def get_messages(thread_id: str):
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        return messages

    @staticmethod
    def chat(message: str) -> str:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful math tutor."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
