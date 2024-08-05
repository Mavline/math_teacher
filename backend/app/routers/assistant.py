# from fastapi import APIRouter, HTTPException
# from app.services.openai_service import OpenAIService
# from app.models.assistant_models import (AssistantCreate,
#                                          AssistantResponse,
#                                          ChatMessage)
# import logging

# logging.basicConfig(level=logging.DEBUG)

# router = APIRouter(prefix="/assistant", tags=["assistant"])


# @router.post("/create", response_model=AssistantResponse)
# def create_assistant(assistant_data: AssistantCreate):
#     try:
#         assistant = OpenAIService.create_assistant(
#             name=assistant_data.name,
#             instructions=assistant_data.instructions
#         )
#         return AssistantResponse(id=assistant.id, name=assistant.name)
#     except ValueError as ve:
#         raise HTTPException(status_code=400, detail=str(ve))
#     except Exception as e:
#         logger = logging.getLogger(__name__)
#         logger.error(f"Error creating assistant: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")


# @router.post("/chat")
# def chat(message: ChatMessage):
#     try:
#         response = OpenAIService.chat(message.content)
#         return {"response": response}
#     except ValueError as ve:
#         raise HTTPException(status_code=400, detail=str(ve))
#     except Exception as e:
#         logger = logging.getLogger(__name__)
#         logger.error(f"Error processing chat message: {str(e)}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

from fastapi import APIRouter, HTTPException
from app.services.openai_service import OpenAIService
from app.models.assistant_models import (AssistantCreate,
                                         AssistantResponse,
                                         ChatMessage)
from app.logger import setup_logging

logger = setup_logging()

router = APIRouter(prefix="/assistant", tags=["assistant"])
openai_service = OpenAIService()


@router.post("/create", response_model=AssistantResponse)
def create_assistant(assistant_data: AssistantCreate):
    try:
        assistant = OpenAIService.create_assistant(
            name=assistant_data.name,
            instructions=assistant_data.instructions
        )
        logger.info(f"Assistant created: {assistant.name}")
        return AssistantResponse(id=assistant.id, name=assistant.name)
    except ValueError as ve:
        logger.warning(f"Invalid input for assistant creation: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error creating assistant: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/chat")
def chat(message: ChatMessage):
    try:
        logger.info(f"Processing chat message: {message.content[:50]}...")
        response = OpenAIService.chat(message.content)
        return {"response": response}
    except ValueError as ve:
        logger.warning(f"Invalid input for chat: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
