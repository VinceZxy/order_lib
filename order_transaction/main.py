# coding=UTF-8
from fastapi import status,FastAPI,Response
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from application.api import application_api
from order.api import order_api

app = FastAPI()

# async def get_token_header(x_token: str = Header(...)):
#     if x_token != "fake-super-secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")

# app.mount("/static", StaticFiles(directory="static"), name="static")  # 挂载静态文件，指定目录


# 注册 APIRouter  路由
app.include_router(application_api.router,prefix="/applications")
app.include_router(order_api.router,prefix="/orders")

origins = [
    "http://192.168.0.115:3000",
    "http://192.168.0.119:3000",
    "http://localhost:3000",
    # "http://localhost.wisdomx.net",
    # "http://localhost",
    # "http://localhost:8080",
]

# 解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="192.168.0.114", port=8001,debug=True)


