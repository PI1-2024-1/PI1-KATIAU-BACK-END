from typing import Union

from fastapi import FastAPI
from controllers.user import testfunc
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get('/user')
def get_user():
    return testfunc()


item_list = {
    '1': 'foo',
    '2': 'bar' 
}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):

    return {"item_id": item_id, "q": q, 'myItem': item_list[str(item_id)]}