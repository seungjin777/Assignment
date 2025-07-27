# 이 아래의 코드는 파이썬에서 fastapi를 사용하기 위해 필요한 모듈들을 가져오는 코드입니다.

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import json
import os
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import RequestValidationError as FastAPIRequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import status

# 이 아래에는 과제 수행에 필요한 공통 코드 및 도구들이 제공됩니다.

# 다음의 코드로 FastAPI 애플리케이션을 만들어서 사용합니다.
app = FastAPI()
# Jinja2는 깊게 알 필요는 없고, 그냥 HTML 안에 데이터를 넣는 용도로 사용합니다.
templates = Jinja2Templates(directory="templates")

# 실 환경에서는 DB에서 데이터를 가져오므로 과제에서 목업 데이터 사용 함수는 기본으로 제공됩니다.
def load_mock_data(filename):
    path = os.path.join(os.path.dirname(__file__), '../data', filename)
    with open(path, encoding='utf-8') as f:
        return json.load(f)
    
def save_mock_data(filename, data):
    path = os.path.join(os.path.dirname(__file__), '../data', filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 마찬가지로 기본 데이터 CRUD 함수들도 제공됩니다.
def create_mock_data_item(filename, item_id, item_data):
    data = load_mock_data(filename)
    if item_id in data:
        return False  # 이미 존재하는 ID
    data[item_id] = item_data
    save_mock_data(filename, data)
    return True

def get_mock_data_item(filename, item_id):
    data = load_mock_data(filename)
    return data.get(item_id, None)  # ID가 없으면 None 반환

def delete_mock_data_item(filename, item_id):
    data = load_mock_data(filename)
    if item_id in data:
        del data[item_id]
        save_mock_data(filename, data)
        return True
    return False

def update_mock_data_item(filename, item_id, new_data):
    data = load_mock_data(filename)
    if item_id in data:
        data[item_id] = new_data
        save_mock_data(filename, data)
        return True
    return False  

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "FastAPI 예제"})

@app.exception_handler(StarletteHTTPException)
async def custom_404_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        # 미구현 과제 안내 페이지 반환
        return templates.TemplateResponse(
            "not_implemented.html",
            {"request": request, "message": "아직 구현 안된 과제입니다!<br>해당 API/페이지는 직접 구현해보세요."},
            status_code=404
        )
    # 그 외 에러는 기본 처리
    return await app.default_exception_handler(request, exc)


# 여기에서부터 과제 코드를 작성해주세요.
# 1단계
@app.get("/hello/{name}", response_class=HTMLResponse)
def get_page(request: Request, name: str):
    return templates.TemplateResponse("hello.html", {"request": request, "name": name})
