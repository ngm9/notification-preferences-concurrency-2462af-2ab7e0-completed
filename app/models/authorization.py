from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import NotificationPreference, User


def get_authorized_preference(
    db: Session,
    current_user: User,
    preference_id: int,
) -> NotificationPreference:
    stmt = (
        select(NotificationPreference)
        .join(
            User,
            User.id == NotificationPreference.user_id,
        )
        .where(
            NotificationPreference.id == preference_id,
            NotificationPreference.tenant_id == current_user.tenant_id,
            User.tenant_id == current_user.tenant_id,
        )
    )

    preference = db.scalar(stmt)

    # Conceal cross-tenant resources instead of confirming they exist.
    if preference is None:
        raise HTTPException(
            status_code=404,
            detail="Notification preferences not found.",
        )

    if (
        current_user.role != "admin"
        and preference.user_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You cannot access another user's preferences.",
        )

    return preference
