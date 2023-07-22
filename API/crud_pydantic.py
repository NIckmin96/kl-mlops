from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

USER_DB = {}

NAME_NOT_FOUND = HTTPException(status_code=400, detail='Name not found')

# Define input Schema -> class
class CreateIn(BaseModel):
    name:str
    nickname:str
    
# Define Output Schema -> class
class CreateOut(BaseModel):
    status:str
    id:int
    
# Response Model : Response Body에 사용될 데이터 모델(Schema) 지정
@app.post("/users", response_model=CreateOut)
def create_user(user:CreateIn) -> CreateOut:
    USER_DB[user.name] = user.nickname
    return CreateOut(status='success', id=len(USER_DB))

@app.get("/users")
def read_user(name:str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    return {"nickname":USER_DB[name]}

@app.put("/users")
def update_user(name:str, nickname:str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    return {"status":"success"}

@app.delete("/users")
def delete_user(name:str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    del USER_DB[name]
    return {"status":"success"}
