from fastapi import APIRouter, status,Request,Form
from logger import logger
from application.service import application_service
from fastapi.responses import JSONResponse
from application.api.application_schema import Application,DeleteApplication,Pre_Page_Application
from typing import List
router = APIRouter()

# 新增系统
@router.post("/", tags=["application"])
async def add_application(app:Application):
    try:
        application = application_service.add_application(app)
    except Exception as e:
        logger.error("新增新增系统(add_application):" + str(e))
        return JSONResponse(content=str("新增系统出错"), status_code=status.HTTP_417_EXPECTATION_FAILED)
    return application
#（排序，过滤 与 分页）
# 查询所有系统信息
#filter_mes  过滤参数,例如：查询某个时间段的订单信息,等具体需求出来再写
@router.get("/", tags=["application"],response_model=Pre_Page_Application)
async def get_applications(page: int, pre_page: int,is_order_by:str=None,filter_mes:str=None):
    try:
        pagination = application_service.get_applications(page,pre_page,is_order_by,filter_mes)
    except Exception as e:
        logger.error("查询所有系统(add_application):" + str(e))
        return JSONResponse(content=str("查询所有系统出错"), status_code=status.HTTP_417_EXPECTATION_FAILED)
    return pagination

# 根据id查询系统信息
@router.get("/{sys_id}", tags=["application"],response_model=Application)
async def get_application_bysysid(sys_id:str):
    try:
        application = application_service.get_application_bysysid(sys_id)
    except Exception as e:
        logger.error("查询系统(add_application):" + str(e))
        return JSONResponse(content=str("查询系统出错"), status_code=status.HTTP_417_EXPECTATION_FAILED)
    return application
# 修改系统信息
@router.put("/{sys_id}", tags=["application"],response_model=Application)
async def updata_applications(sys_id:str,app:Application):
    try:
         application_service.updata_applications(sys_id,app)
    except Exception as e:
        logger.error("查询系统(add_application):" + str(e))
        return JSONResponse(content=str("查询系统出错"), status_code=status.HTTP_417_EXPECTATION_FAILED)
    return JSONResponse(content=str("修改完成"), status_code=status.HTTP_417_EXPECTATION_FAILED)
# 删除系统信息
@router.delete("/{sys_id}", tags=["application"])
async def del_applications(sys_id:str):
    try:
         application_service.del_applications(sys_id)
    except Exception as e:
        logger.error("删除系统(add_application):" + str(e))
        return JSONResponse(content=str("删除系统出错"), status_code=status.HTTP_417_EXPECTATION_FAILED)
    return JSONResponse(content=str("删除完成"), status_code=status.HTTP_417_EXPECTATION_FAILED)



