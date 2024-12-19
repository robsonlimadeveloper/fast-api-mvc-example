from pydantic import BaseModel, Field, constr

class AuthDTORequest(BaseModel):
    """Auth login DTO"""
    username: str = Field(..., max_length=50, description="Username for authentication")
    password: str = Field(..., max_length=255, description="Password for authentication")

class AuthDTOResponse(BaseModel):
    """Auth token DTO"""
    access_token: str = Field(..., description="Authentication token")
    token_type: str = Field(..., description="Token type")

class AuthUserDTO(BaseModel):
    """Auth user DTO"""
    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    password: str = Field(..., description="User's password")

class TokenData(BaseModel):
    user_id: int = Field(..., description="User ID")
