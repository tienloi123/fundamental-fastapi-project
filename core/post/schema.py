from pydantic import BaseModel

class CreateUpdatePost(BaseModel):
    title:str
    content:str