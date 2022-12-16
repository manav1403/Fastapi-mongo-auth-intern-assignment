from models.models import Todo, User
from database.database import collection_name, user_db

from schemas.schemas import todos_serializer
from bson import ObjectId

from fastapi import APIRouter, HTTPException, Depends, status
from auth.hash import Hash
from auth.jwt import create_access_token
from auth.oauth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

todo_api_router = APIRouter(prefix = "/api/todos")
user_api_router = APIRouter(prefix = "/api/user")

# retrieve
@todo_api_router.get("/")
async def get_todos(current_user:User = Depends(get_current_user)):
    todos = todos_serializer(collection_name.find())
    return todos

@todo_api_router.get("/{uid}")
async def get_todo(uid, current_user:User = Depends(get_current_user)):
    return todos_serializer(collection_name.find_one({"_id": ObjectId(uid)}))


# post
@todo_api_router.post("/")
async def create_todo(todo: Todo, current_user:User = Depends(get_current_user)):
    _id = collection_name.insert_one(dict(todo))
    return todos_serializer(collection_name.find({"_id": _id.inserted_id}))


# update
@todo_api_router.put("/{uid}")
async def update_todo(uid: str, todo: Todo, current_user:User = Depends(get_current_user)):
    collection_name.find_one_and_update({"_id": ObjectId(uid)}, {
        "$set": dict(todo)
    })
    return todos_serializer(collection_name.find({"_id": ObjectId(id)}))

# delete
@todo_api_router.delete("/{uid}")
async def delete_todo(uid: str, current_user:User = Depends(get_current_user)):
    collection_name.find_one_and_delete({"_id": ObjectId(uid)})
    return {"status": "ok"}



# @user_api_router.get("/")
# def read_root(current_user:User = Depends(get_current_user)):
# 	return {"data":"Hello OWrld"}

@user_api_router.post('/register')
def create_user(request:User):
    hashed_pass = Hash.bcrypt(request.password)
    user_object = dict(request)
    user_object["password"] = hashed_pass
    _ = user_db["users"].insert(user_object)
    # print(user)
    return {"res":"created"}

@user_api_router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends()):
    user = user_db["users"].find_one({"username":request.username})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'No user found with this {request.username} username')
    if not Hash.verify(user["password"],request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f'Wrong Username or password')
    access_token = create_access_token(data={"sub": user["username"] })
    return {"access_token": access_token, "token_type": "bearer"}