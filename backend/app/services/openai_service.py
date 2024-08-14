from openai import OpenAI
from app.config import settings
from typing import List, Optional, Union
import time
from app.models.assistant_models import ContentItem
from app.logger import setup_logging

logger = setup_logging()


client = OpenAI(api_key=settings.OPENAI_API_KEY)


class OpenAIService:
    @staticmethod
    def create_assistant(name: str, instructions: str, model: str, tools: Optional[List[dict]] = None):
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
            tools=tools or [{"type": "code_interpreter"}, {"type": "file_search"}],
            tool_resources={
                "code_interpreter": {
                    "file_ids": []  # We'll add file IDs here when needed
                }
            }
        )
        return assistant

    @staticmethod
    def create_thread():
        return client.beta.threads.create()

    @staticmethod
    def upload_file(file_path: str, purpose: str):
        with open(file_path, "rb") as file:
            response = client.files.create(file=file, purpose=purpose)
        logger.info(f"File uploaded to OpenAI: {file_path} with ID: {response.id}")
        return response

    @staticmethod
    def add_message_to_thread(thread_id: str, content: Union[str, List[ContentItem]], file_ids: Optional[List[str]] = None):
        if isinstance(content, str):
            message_content = [{"type": "text", "text": content}]
        else:
            message_content = content

        if file_ids:
            for file_id in file_ids:
                message_content.append({
                    "type": "image_file",
                    "image_file": {"file_id": file_id}
                })
        
        message_params = {
            "thread_id": thread_id,
            "role": "user",
            "content": message_content
        }
        
        return client.beta.threads.messages.create(**message_params)

    @staticmethod
    def run_assistant(thread_id: str, assistant_id: str, instructions: Optional[str] = None):
        run_params = {
            "thread_id": thread_id,
            "assistant_id": assistant_id,
        }
        if instructions:
            run_params["instructions"] = instructions
        
        return client.beta.threads.runs.create(**run_params)

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
    def chat(thread_id: str, assistant_id: str, content: Union[str, List[ContentItem]], file_ids: Optional[List[str]] = None, instructions: Optional[str] = None):
        try:
            OpenAIService.add_message_to_thread(thread_id, content, file_ids)
            run = OpenAIService.run_assistant(thread_id, assistant_id, instructions)
            OpenAIService.wait_for_run_completion(thread_id, run.id)
            messages = OpenAIService.get_messages(thread_id)
            
            # Process annotations and citations
            latest_message = messages.data[0]
            message_content = latest_message.content[0].text
            annotations = message_content.annotations
            citations = []

            for index, annotation in enumerate(annotations):
                message_content.value = message_content.value.replace(annotation.text, f' [{index}]')
                if (file_citation := getattr(annotation, 'file_citation', None)):
                    cited_file = client.files.retrieve(file_citation.file_id)
                    citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
                elif (file_path := getattr(annotation, 'file_path', None)):
                    cited_file = client.files.retrieve(file_path.file_id)
                    citations.append(f'[{index}] Click to download {cited_file.filename}')

            message_content.value += '\n' + '\n'.join(citations)
            return message_content.value
        except Exception as e:
            logger.error(f"Error in OpenAIService.chat: {str(e)}", exc_info=True)
            raise
