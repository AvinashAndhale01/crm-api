from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.modules.notes.model import Note
from app.modules.notes.schema import (
    CreateNote,
    UpdateNote,
    MessageResponse,
    PaginatedNoteResponse,
)
from app.modules.users.model import User


def _get_note_by_id(note_id: int, session: Session, current_user: User) -> Note:
    note = (
        session.query(Note)
        .filter(
            Note.id == note_id,
            Note.created_by_id == current_user.id,
        )
        .first()
    )
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Note not found"
        )
    return note


def get_note(note_id: int, session: Session, current_user: User) -> Note:
    note = _get_note_by_id(note_id, session, current_user)
    return note


def get_notes(
    session: Session, limit: int, offset: int, current_user: User
) -> PaginatedNoteResponse:
    total = session.query(Note).filter(Note.created_by_id == current_user.id).count()
    notes = (
        session.query(Note)
        .filter(Note.created_by_id == current_user.id)
        .order_by(Note.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return PaginatedNoteResponse(total=total, limit=limit, offset=offset, items=notes)


def create_note(note: CreateNote, session: Session, current_user: User) -> Note:
    db_note = Note(**note.model_dump(), created_by_id=current_user.id)
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note


def update_note(
    note_id: int,
    note: UpdateNote,
    session: Session,
    current_user: User,
) -> Note:
    existing_note = _get_note_by_id(note_id, session, current_user)
    for key, value in note.model_dump(exclude_unset=True).items():
        setattr(existing_note, key, value)
    session.commit()
    session.refresh(existing_note)
    return existing_note


def delete_note(note_id: int, session: Session, current_user: User) -> MessageResponse:
    existing_note = _get_note_by_id(note_id, session, current_user)
    session.delete(existing_note)
    session.commit()
    return MessageResponse(detail="Note deleted successfully")
