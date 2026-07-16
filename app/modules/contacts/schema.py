from pydantic import BaseModel, ConfigDict


class ContactBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(ContactBase):
    pass


class ContactResponse(ContactBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedContactsResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[ContactResponse]
