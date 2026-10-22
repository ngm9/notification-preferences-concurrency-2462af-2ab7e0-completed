class NotificationPreference(Base):
    __tablename__ = "notification_preferences"
    __table_args__ = (
        UniqueConstraint("tenant_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True,
    )

    email_enabled: Mapped[bool] = mapped_column(
        Boolean, default=True
    )
    sms_enabled: Mapped[bool] = mapped_column(
        Boolean, default=False
    )
    push_enabled: Mapped[bool] = mapped_column(
        Boolean, default=True
    )
    version: Mapped[int] = mapped_column(
        Integer, nullable=False, default=1
    )
