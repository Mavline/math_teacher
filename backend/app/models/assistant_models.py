from pydantic import BaseModel


class AssistantCreate(BaseModel):
    name: str
    instructions: str


class AssistantResponse(BaseModel):
    id: str
    name: str


class ChatMessage(BaseModel):
    content: str
