from typing import TypedDict


class ThreadCreate(TypedDict):
    pass


class ThreadResponse(TypedDict):
    id: str


class MessageCreate(TypedDict):
    content: str


class MessageResponse(TypedDict):
    id: str
    content: str


class RunCreate(TypedDict):
    assistant_id: str


class RunResponse(TypedDict):
    id: str
    status: str
