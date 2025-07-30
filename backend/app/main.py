# 이 아래의 코드는 파이썬에서 fastapi를 사용하기 위해 필요한 모듈들을 가져오는 코드입니다.

from fastapi import FastAPI, Request, Form
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

def new_create_mock_data_item(filename, item_id, item_data):
    # 방법이 정확하지 않아 따로 수정하지 않음
    return

# ------------------------------------------------------------------    
def get_mock_data_item(filename, item_id):
    data = load_mock_data(filename)
    return data.get(item_id, None)  # ID가 없으면 None 반환 

def new_get_mock_data_item(filename, item_id):
    datas = load_mock_data(filename)
    for data in datas:
        if data['id'] == item_id:
            return data
    return None
# ------------------------------------------------------------------    
def delete_mock_data_item(filename, item_id):
    data = load_mock_data(filename)
    if item_id in data:
        del data[item_id]
        save_mock_data(filename, data)
        return True
    return False

def new_delete_mock_data_item(filename, item_id):
    datas = load_mock_data(filename)              
    for idx, data in enumerate(datas, start=0):     
        if data["id"] == item_id:                 # 기존 데이터 존재 확인
            del datas[idx]
            break
        else:
            return "delete fail"            
    save_mock_data(filename, datas) # 저장
    return "delete Success"

# ------------------------------------------------------------------    
def update_mock_data_item(filename, item_id, new_data):
    data = load_mock_data(filename)
    if item_id in data:
        data[item_id] = new_data
        save_mock_data(filename, data)
        return True
    return False  

def new_update_mock_data_item(filename, item_id, newRow):
    datas = load_mock_data(filename)              
    for idx, data in enumerate(datas, start=0):     
        if data["id"] == item_id:                 # 기존 데이터 존재 확인
            datas[idx] = newRow
            break
        else:
            return "put fail"            
    save_mock_data(filename, datas) # 저장
    return "put Success"
# ------------------------------------------------------------------    

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
# 1단계--------------------------------------------------------------------------------
@app.get("/hello/{name}", response_class=HTMLResponse)
def get_page(request: Request, name: str):
    return templates.TemplateResponse("hello.html", {"request": request, "name": name})


# 2단계--------------------------------------------------------------------------------
# user.json파일에서 데이터를 받아와 user.html로 넘겨주는 코드를 작성해야함
@app.get("/users", response_class=JSONResponse)
def get_users(request: Request):
    with open('./data/users.json') as file:  # users.json파일 불러옴
        users = json.load(file)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/products", response_class=JSONResponse)
def get_products(request: Request):
    with open('./data/products.json') as file:  # products.json파일 불러옴
        products = json.load(file)
    return templates.TemplateResponse("products.html", {"request": request, "products": products})


# 3단계--------------------------------------------------------------------------------
# join 필요(불가능)?, purchases에서 id, user_id로 각각 데이터 추출
# 이미 작성된 데이터 추출 함수가 있었음
@app.get("/summary", response_class=JSONResponse)
def get_purchases(request: Request):
    
    # 조합할 데이터 준비
    purchases = load_mock_data("purchases.json")
    products = load_mock_data("products.json")
    users = load_mock_data("users.json")

    purchases_summary = purchases   # 조합할 데이터 복제
    # purchases에서 user_id와 일치하는 user데이터 삽입
    # purchases에서 id와 일치하는 product데이터 삽입
    # o(n^2) 이게 맞나? 예외 처리도 필요할듯
    for idx, purchase in enumerate(purchases_summary, start=0):
        for user in users:
            if(user.get('id', None) == purchase['user_id']):
                purchases_summary[idx]['user_name'] = user['name']
                    
        for product in products:
            if(product.get('id', None) == purchase['product_id']):
                purchases_summary[idx]['product_name'] = product['name']
                purchases_summary[idx]['product_price'] = product['price']
    return templates.TemplateResponse("summary.html", {"request": request, "purchases": purchases_summary})


# 4단계--------------------------------------------------------------------------------
# get
@app.get("/user_create", response_class=HTMLResponse)
def get_userCreate(request: Request):
    return templates.TemplateResponse("user_create.html", {"request": request})

@app.get("/product_create", response_class=HTMLResponse)
def get_productCreate(request: Request):
    return templates.TemplateResponse("product_create.html", {"request": request})

@app.get("/purchase_create", response_class=HTMLResponse)
def purchaseCreate(request: Request):
    return templates.TemplateResponse("purchase_create.html", {"request": request})

#post
@app.post("/users")
def create_user(name: str = Form(), email: str = Form()):    
    userForm =load_mock_data("users.json")              # 기존 데이터 받아옴
    idx =  userForm[len(userForm)-1]['id'] + 1    # 기존 데이터 길이 + 1 
    # -----> 잘못된 방법일듯 id값이 정렬되지 않은 경우 or 각 id값이 index와 일치하지 않는 경우 문제 발생
    newRow = {'id': idx, 'name': name, 'email': email}  # 새로 삽입할 데이터 생성
    userForm.append(newRow)                             # 기존 데이터에 새데이터 추가
    save_mock_data("users.json", userForm)              # 저장
    return "post Success" 

@app.post("/products")
def create_products(name: str = Form(), price: str = Form()):
    productForm =load_mock_data("products.json") 
    idx = productForm[len(productForm)-1]['id'] + 1
    newRow = {'id': idx, 'name': name, 'price': price}
    productForm.append(newRow)
    save_mock_data("products.json", productForm)
    return "post Success"

@app.post("/purchases")
def create_products(user_id: int = Form(), product_id: int = Form(), date: str = Form()):
    purchaseForm =load_mock_data("purchases.json") 
    idx = purchaseForm[len(purchaseForm)-1]['id'] + 1
    newRow = {'id': idx, 'user_id': user_id, 'product_id': product_id, 'date': date}
    purchaseForm.append(newRow)
    save_mock_data("purchases.json", purchaseForm)
    return "post Success"


# 5단계--------------------------------------------------------------------------------
# get
@app.get("/user_edit/{id}", response_class=HTMLResponse)
def get_userEdit(request: Request, id: int):
    # user = get_mock_data_item("users.json", id) # 리스트는 get() 사용x --> 새로 만듦
    user = new_get_mock_data_item("users.json", id)
    if(user == None):            # 예외처리
        return "user Get Fail"           
    return templates.TemplateResponse("user_edit.html", {"request": request, "user" : user})

@app.get("/product_edit/{id}", response_class=HTMLResponse)
def get_productEdit(request: Request, id: int):
    product = new_get_mock_data_item("products.json", id)
    if(product == None):            # 예외처리
        return "product Get Fail"         
    return templates.TemplateResponse("product_edit.html", {"request": request, "product" : product})

@app.get("/purchase_edit/{id}", response_class=HTMLResponse)
def get_purchaseEdit(request: Request, id: int):
    purchase = new_get_mock_data_item("purchases.json", id)
    if(purchase == None):            # 예외처리
        return "purchase Get Fail"
    return templates.TemplateResponse("purchase_edit.html", {"request": request, "purchase" : purchase})

# 수정
# HTML 폼(form) 요청이 PUT, DELETE를 지원하지 않는다. 
# 좀 이상한 방법? --> post로 받아 쿼리에서 method 확인후 put, delete실행
@app.post("/users/{id}") 
def put_delete_user(request: Request, id: int, name: str = Form(None), email: str = Form(None)):
    method = request.query_params.get("_method")
    if method == "put":
        newRow = {'id': id, 'name': name, 'email':email}  # 새로 변경할 데이터
        return new_update_mock_data_item("users.json", id, newRow) # 업데이트
    elif method == "delete":
        return new_delete_mock_data_item("users.json", id) # 삭제
    else:
        return "method Error!"

@app.post("/products/{id}") 
def put_delete_product(request: Request, id: int, name: str = Form(None), price: str = Form(None)):
    method = request.query_params.get("_method")
    if method == "put":
        newRow = {'id': id, 'name': name, 'price':price}  # 새로 변경할 데이터
        return new_update_mock_data_item("products.json", id, newRow) # 업데이트
    elif method == "delete":
        return new_delete_mock_data_item("products.json", id) # 삭제
    else:
        return "method Error!"
    
@app.post("/purchases/{id}") 
def put_delete_product(request: Request, id: int, user_id: int = Form(None),
                       product_id: int = Form(None), date: str = Form(None)):
    method = request.query_params.get("_method")
    if method == "put":
        newRow = {'id': id, 'user_id': user_id, 'product_id':product_id, 'date': date}  # 새로 변경할 데이터
        return new_update_mock_data_item("purchases.json", id, newRow) # 업데이트
    elif method == "delete":
        return new_delete_mock_data_item("purchases.json", id) # 삭제
    else:
        return "method Error!"