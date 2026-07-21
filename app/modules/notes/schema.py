from pydantic import BaseModel, ConfigDict


class NoteBase(BaseModel):
    content: str


class CreateNote(NoteBase):
    lead_id: int


class UpdateNote(BaseModel):
    content: str | None = None
    

class NoteResponse(NoteBase):
    id: int
    lead_id: int
    created_by_id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedNoteResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[NoteResponse]


class MessageResponse(BaseModel):
    detail: str
