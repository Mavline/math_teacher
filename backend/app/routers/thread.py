# from fastapi import APIRouter, HTTPException
# from app.services.openai_service import OpenAIService
# from app.models.thread_models import (MessageCreate, RunCreate, ThreadResponse,
#                                       MessageResponse, RunResponse)

# router = APIRouter(prefix="/thread", tags=["thread"])


# @router.post("/create", response_model=ThreadResponse)
# async def create_thread():
#     try:
#         thread = await OpenAIService.create_thread()
#         return ThreadResponse(id=thread.id)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/{thread_id}/message", response_model=MessageResponse)
# async def add_message(thread_id: str, message_data: MessageCreate):
#     try:
#         message = await OpenAIService.add_message_to_thread(
#             thread_id, message_data["content"])
#         return MessageResponse(id=message.id, content=message.content)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/{thread_id}/run", response_model=RunResponse)
# async def run_assistant(thread_id: str, run_data: RunCreate):
#     try:
#         run = await OpenAIService.run_assistant(
#             thread_id, run_data["assistant_id"])
#         return RunResponse(id=run.id, status=run.status)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/{thread_id}/run/{run_id}", response_model=RunResponse)
# async def get_run_status(thread_id: str, run_id: str):
#     try:
#         run = await OpenAIService.get_run_status(thread_id, run_id)
#         return RunResponse(id=run.id, status=run.status)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.get("/{thread_id}/messages")
# async def get_messages(thread_id: str):
#     try:
#         messages = await OpenAIService.get_messages(thread_id)
#         return [MessageResponse(
#             id=msg.id, content=msg.content) for msg in messages.data]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


from fastapi import APIRouter, HTTPException
from app.services.openai_service import OpenAIService
from app.models.thread_models import (MessageCreate, RunCreate, ThreadResponse,
                                      MessageResponse, RunResponse)

router = APIRouter(prefix="/thread", tags=["thread"])


@router.post("/create", response_model=ThreadResponse)
async def create_thread():
    try:
        thread = OpenAIService.create_thread()
        return ThreadResponse(id=thread.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{thread_id}/message", response_model=MessageResponse)
async def add_message(thread_id: str, message_data: MessageCreate):
    try:
        message = OpenAIService.add_message_to_thread(
            thread_id, message_data.content)
        return MessageResponse(id=message.id, content=message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{thread_id}/run", response_model=RunResponse)
async def run_assistant(thread_id: str, run_data: RunCreate):
    try:
        run = OpenAIService.run_assistant(
            thread_id, run_data.assistant_id)
        return RunResponse(id=run.id, status=run.status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{thread_id}/run/{run_id}", response_model=RunResponse)
async def get_run_status(thread_id: str, run_id: str):
    try:
        run = OpenAIService.get_run_status(thread_id, run_id)
        return RunResponse(id=run.id, status=run.status)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{thread_id}/messages")
async def get_messages(thread_id: str):
    try:
        messages = OpenAIService.get_messages(thread_id)
        return [MessageResponse(
            id=msg.id, content=msg.content) for msg in messages.data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
