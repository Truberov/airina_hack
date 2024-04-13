from pydantic import BaseModel


class ClassifyDocumentRequest(BaseModel):
    content: str
