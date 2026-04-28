from pydantic import BaseModel

class SignupModel(BaseModel):
    name: str
    email: str
    password: str

class LoginModel(BaseModel):
    email: str
    password: str
    
class AskModel(BaseModel):
    question: str
    
class MessageCreate(BaseModel):
    thread_id: int
    message: str
    
class ThreadCreate(BaseModel):
    title: str