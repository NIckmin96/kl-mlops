from fastapi import FastAPI, HTTPException

app = FastAPI()

USER_DB = {}

NAME_NOT_FOUND = HTTPException(status_code=400, detail="Name not Found.")

# PATH parameter

# Create(C)
@app.post("/users/name/{name}/nickname/{nickname}")
def create_user(name:str, nickname:str):
    USER_DB[name] = nickname
    return {"status":"success"}

# Read(R)
@app.get("/users/name/{name}")
def read_user(name:str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    return {"nickname":USER_DB[name]}

# Update(U)
@app.put("/users/name/{name}/nickname/{nickname}")
def update_user(name:str, nickname:str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    USER_DB[name] = nickname
    return {"status":"success"}

# Delete(D)
@app.delete("/users/name/{name}")
def delete_user(name:str):
    if name not in USER_DB:
        raise NAME_NOT_FOUND
    del USER_DB[name]
    return {"status":"success"}

print(create_user('bokki', 'bk'))
print(read_user('bokki'))
print(update_user('bokki', 'king'))
print(read_user('bokki'))
print(delete_user('bokki'))
print(read_user('bokki'))