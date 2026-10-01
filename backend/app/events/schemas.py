from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


NotificationSeverity = Literal["low", "medium", "high", "critical"]


class NotificationRead(BaseModel):
    id: int
    event_type: str
    severity: NotificationSeverity
    title: str
    message: str
    entity_type: str | None
    entity_id: int | None
    payload: dict
    read_at: datetime | None
    created_at: datetime


class NotificationPage(BaseModel):
    items: list[NotificationRead]
    unread_count: int
    next_after_id: int | None = None


class EventRead(BaseModel):
    id: int
    entity_type: str
    entity_id: int
    action: str
    actor_type: str
    actor_user_id: int | None
    payload: dict
    created_at: datetime


class EventPage(BaseModel):
    items: list[EventRead]
    next_after_id: int | None = None


class MarkReadRequest(BaseModel):
    read: bool = True
