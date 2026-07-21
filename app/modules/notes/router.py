from fastapi import APIRouter, status, Query, Depends
from app.modules.notes import service
from app.modules.notes.schema import (
    CreateNote,
    UpdateNote,
    NoteResponse,
    MessageResponse,
    PaginatedNoteResponse,
)
from app.modules.users.model import User
from app.dependencies.db import SessionDep
from app.dependencies.auth import get_current_user


router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(
    note_id: int,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    return service.get_note(note_id, session, current_user)


@router.get("/", response_model=PaginatedNoteResponse)
def get_notes(
    session: SessionDep,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
):
    return service.get_notes(session, limit, offset, current_user)


@router.post(
    "/",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    note: CreateNote,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    return service.create_note(note, session, current_user)


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(
    note_id: int,
    note: UpdateNote,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    updated_note = service.update_note(note_id, note, session, current_user)
    return updated_note


@router.delete(
    "/{note_id}", response_model=MessageResponse, status_code=status.HTTP_200_OK
)
def delete_note(
    note_id: int, session: SessionDep, current_user: User = Depends(get_current_user)
):
    return service.delete_note(note_id, session, current_user)
