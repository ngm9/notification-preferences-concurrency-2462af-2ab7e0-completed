from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class PreferencePatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email_enabled: bool | None = None
    sms_enabled: bool | None = None
    push_enabled: bool | None = None
    version: int = Field(ge=1)


class PreferenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    email_enabled: bool
    sms_enabled: bool
    push_enabled: bool
    version: int
