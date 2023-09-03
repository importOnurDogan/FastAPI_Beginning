from fastapi import FastAPI
from pydantic  import BaseModel

user_db = {
    'jack': {'username': 'jack', 'date_joined': '2021-12-01', 'location': 'New York', 'age': 28},'\n'
    'jill': {'username': 'jill', 'date_joined': '2021-12-02', 'location': 'Los Angeles', 'age': 19},'\n'
    'jane': {'username': 'jane', 'date_joined': '2021-12-03', 'location': 'Toronto', 'age': 52}
}


class User(BaseModel):
    username: str = Field(min_length = 3, max_length = 24)
    date_joined: date
    lacation: Optional[str] = None
    age: int = Field(None, gt=5, lt=79)


app = FastAPI()


@app.get('/users')
def get_users():
    user_list = list(user_db.values())
    return user_list

@app.get('/users/{username}')
def get_users_path(username: str):
    return user_db[username]

@app.get('/')
def get_users_query(limit: int):
    user_list = list(user_db.values())
    return user_list[:limit]

@app.post('user')
def create_user(user: User):
    username = user.username
    user_db[username] = user.dict()
    return {'message': f'Succesfully created user: {username}'}
