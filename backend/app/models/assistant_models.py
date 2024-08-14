from pydantic import BaseModel
from typing import List, Optional, Union


class ContentItem(BaseModel):
    type: str
    text: Optional[str] = None
    image_file: Optional[dict] = None


class Attachment(BaseModel):
    file_id: str


class AssistantCreate(BaseModel):
    name: str
    instructions: str
    model: str = "gpt-4o-mini"
    tools: Optional[List[dict]] = None


class AssistantResponse(BaseModel):
    id: str
    name: str
    instructions: str
    model: str
    tools: List[dict]


class ChatMessage(BaseModel):
    content: Union[str, List[ContentItem]]
    assistant_id: str
    session_id: Optional[str] = None
    attachments: Optional[List[Attachment]] = None
    instructions: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    session_id: str
