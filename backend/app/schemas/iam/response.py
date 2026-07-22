from pydantic import BaseModel


class ScanResponse(BaseModel):
    message: str