from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional


class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="Email of the user")
    dni: int = Field(..., ge=1000, le=999999999999, description="DNI of the user")
    password: str = Field(..., min_length=5, max_length=50, description="Password of the user")
    # algorand_address: str = Field(..., min_length=1, max_length=120, description="Algorand address of the user")
    # algorand_mnemonic: str = Field(..., min_length=1, max_length=250, description="Algorand mnemonic of the user")
    # algorand_private_key: str = Field(..., min_length=1, max_length=250, description="Algorand private key of the user")


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    
class UserOut(BaseModel):
    user_id: UUID
    dni: int
    email: EmailStr
    algorand_address: Optional[str]
    algorand_mnemonic: Optional[str]
    # algorand_private_key: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    disabled: Optional[bool] = False


class UserOutVote(BaseModel):
    id: str
    dni: int
    email: EmailStr
    algorand_address: Optional[str]
    algorand_mnemonic: Optional[str]
    # algorand_private_key: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    disabled: Optional[bool] = False

