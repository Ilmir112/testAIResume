from pydantic import BaseModel


class SResumes(BaseModel):
    title: str
    context: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class SResumesHistory(BaseModel):
    title: str
    context: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
