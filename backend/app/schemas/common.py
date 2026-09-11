"""Common schemas used across the application"""
from pydantic import BaseModel
from typing import Optional

class ErrorResponse(BaseModel):
    """Standard error response"""
    message: str
    code: Optional[str] = None
    details: Optional[dict] = None

class SuccessResponse(BaseModel):
    """Standard success response"""
    message: str
    data: Optional[dict] = None
