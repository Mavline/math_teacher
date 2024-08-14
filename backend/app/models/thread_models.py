from pydantic import BaseModel
from typing import List, Optional, Union


class ContentItem(BaseModel):
    type: str
    text: Optional[str] = None
    image_file: Optional[dict] = None


class Attachment(BaseModel):
    file_id: str


class MessageCreate(BaseModel):
    role: str = "user"
    content: Union[str, List[ContentItem]]
    file_ids: Optional[List[str]] = None


class ThreadCreate(BaseModel):
    messages: Optional[List[MessageCreate]] = None


class RunCreate(BaseModel):
    assistant_id: str
    model: Optional[str] = None
    instructions: Optional[str] = None
    tools: Optional[List[dict]] = None


class ThreadResponse(BaseModel):
    id: str


class MessageResponse(BaseModel):
    id: str
    thread_id: str
    role: str
    content: List[ContentItem]


class RunResponse(BaseModel):
    id: str
    thread_id: str
    assistant_id: str
    status: str
    model: str
