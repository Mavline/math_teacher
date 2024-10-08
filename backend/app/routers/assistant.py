import os
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.openai_service import OpenAIService
from app.models.assistant_models import (AssistantCreate,
                                         AssistantResponse,
                                         ChatMessage,
                                         ChatResponse)
from app.logger import setup_logging

logger = setup_logging()

router = APIRouter(prefix="/assistant", tags=["assistant"])

assistants = {}
threads = {}

@router.post("/create", response_model=AssistantResponse)
def create_assistant(assistant_data: AssistantCreate):
    try:
        assistant = OpenAIService.create_assistant(
            name=assistant_data.name,
            instructions=assistant_data.instructions,
            model=assistant_data.model,
            tools=assistant_data.tools
        )
        assistants[assistant.id] = assistant
        logger.info(f"Assistant created: {assistant.name}")
        return AssistantResponse(**assistant.model_dump())
    except Exception as e:
        logger.error(f"Error creating assistant: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    upload_dir = os.path.join(os.getcwd(), "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Determine the purpose based on file type
        purpose = "assistants" if file.filename.endswith(('.csv', '.txt', '.pdf')) else "vision"
        logger.info(f"Temporary file saved locally: {file_path}")
        uploaded_file = OpenAIService.upload_file(file_path, purpose)
        logger.info(f"File uploaded successfully to OpenAI: {uploaded_file.id}")
        return {"file_id": uploaded_file.id}
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Local file removed: {file_path}")

@router.post("/chat", response_model=ChatResponse)
def chat(chat_message: ChatMessage):
    try:
        if chat_message.session_id is None or chat_message.session_id not in threads:
            thread = OpenAIService.create_thread()
            threads[thread.id] = thread
            chat_message.session_id = thread.id
        
        logger.info(f"Processing chat message: {chat_message.content[:50]}...")
        logger.info(f"Attachments: {chat_message.attachments}")
        
        file_ids = [attachment.file_id for attachment in chat_message.attachments] if chat_message.attachments else None
        logger.info(f"Extracted file_ids: {file_ids}")
        
        response = OpenAIService.chat(
            chat_message.session_id,
            chat_message.assistant_id,
            chat_message.content,
            file_ids,
            chat_message.instructions
        )
        logger.info(f"Received response from OpenAI: {response[:50]}...")
        return ChatResponse(response=response, session_id=chat_message.session_id)
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
