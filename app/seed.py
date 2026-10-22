from sqlalchemy import select

from app.auth import hash_password
from app.database import Base, SessionLocal, engine
from app.models import NotificationPreference, User

Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    if db.scalar(select(User.id).limit(1)) is not None:
        print("Database already contains users; skipping seed.")
        raise SystemExit(0)

    alice = User(
        tenant_id=1,
        email="alice@example.com",
        password_hash=hash_password("Alice-Local-123!"),
        role="user",
    )
    bob = User(
        tenant_id=1,
        email="bob@example.com",
        password_hash=hash_password("Bob-Local-123!"),
        role="admin",
    )
    charlie = User(
        tenant_id=2,
        email="charlie@example.com",
        password_hash=hash_password("Charlie-Local-123!"),
        role="user",
    )
    company_b_admin = User(
        tenant_id=2,
        email="admin-b@example.com",
        password_hash=hash_password("Admin-B-Local-123!"),
        role="admin",
    )

    db.add_all([alice, bob, charlie, company_b_admin])
    db.flush()

    db.add_all([
        NotificationPreference(
            tenant_id=1,
            user_id=alice.id,
            email_enabled=True,
            sms_enabled=False,
            push_enabled=True,
            version=1,
        ),
        NotificationPreference(
            tenant_id=1,
            user_id=bob.id,
            email_enabled=True,
            sms_enabled=True,
            push_enabled=True,
            version=1,
        ),
        NotificationPreference(
            tenant_id=2,
            user_id=charlie.id,
            email_enabled=False,
            sms_enabled=True,
            push_enabled=False,
            version=1,
        ),
        NotificationPreference(
            tenant_id=2,
            user_id=company_b_admin.id,
            email_enabled=True,
            sms_enabled=False,
            push_enabled=True,
            version=1,
        ),
    ])

    db.commit()

    print("Development users and preferences created.")
