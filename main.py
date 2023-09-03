from fastapi import FastAPI
from pydantic  import BaseModel, Field
from typing import Optional
from datetime import date

user_db = {
    'jack': {'username': 'jack', 'date_joined': '2021-12-01', 'location': 'New York', 'age': 28},'\n'
    'jill': {'username': 'jill', 'date_joined': '2021-12-02', 'location': 'Los Angeles', 'age': 19},'\n'
    'jane': {'username': 'jane', 'date_joined': '2021-12-03', 'location': 'Toronto', 'age': 52}
}

class User(BaseModel):
    username: str = Field(min_length=3, max_length=24)
    date_joined: date
    lacation: Optional[str] = None
    age: int = Field(None, gt=5, lt=130)


app = FastAPI()

#Showing the users
@app.get('/users')
def get_users_query(limit: int):
    user_list = list(user_db.values())
    return user_list[:limit]


# Showing the selected user
@app.get('/users/{username}')
def get_users_path(username: str):
    if username not in user_db:
        return False
    return user_db[username]


# Creating new user
@app.post('/users')
def create_user(user: User):
    username = user.username
    if username in user_db:
        return False
    user_db[username] = user.dict()
    return {'message': f'Succesfully created user: {username}'}


# Deleting the user
@app.delete('/users/{username}')
def delete_user(username: str):
    del user_db[username]
    return {'message':f'Successfully deleted user:{username}'}


# Update the User
@app.put('/users')
def update_user(user: User):
    username = user.username
    user_db[username] = user.dict()
    return {'message':f'Successfully updated user:{username}'}


# Update the user's selected attribute
@app.patch('/users')
def update_user_partial(user: User):
    username = user.username
    user_db[username].update(user.dict())
    return {'message':f'Successfully updated user:{username}'}
