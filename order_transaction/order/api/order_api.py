from fastapi import APIRouter,status,Request,Form
from order.api.order_schema import OrderParam,GetOrder,Pre_Page_Order
from fastapi.responses import JSONResponse
from order.service import order_service
from logger import logger
router = APIRouter()

# 新增订单
@router.post("/", tags=["orders"])
async def add_order(app:OrderParam):
    try:
        order_info = order_service.add_order(app)
    except Exception as e:
        logger.error("新增订单接口(add_order):"+str(e))
        return JSONResponse(content=str("订单信息出错"), status_code=status.HTTP_417_EXPECTATION_FAILED)
    return order_info

#（排序，过滤 与 分页）
# 查询所有订单
@router.get("/", tags=["orders"],response_model=Pre_Page_Order)
async def get_orders(page: int, pre_page: int,is_order_by:str=None,filter_mes:str=None):
    try:
        pagination = order_service.get_orders(page,pre_page,is_order_by,filter_mes)
    except Exception as e:
        logger.error("查询所有订单接口(get_orders):"+str(e))
        return JSONResponse(content=str("查询所有订单出错"), status_code=status.HTTP_417_EXPECTATION_FAILED)
    return pagination

# 根据id查询该订单
@router.post("/getOrderById", tags=["orders"])
async def get_order_id(app:OrderParam):
    try:
        order_info = order_service.get_order_id(app)
    except Exception as e:
        logger.error("根据id查询该订单接口(get_order_id):"+str(e))
        return JSONResponse(content=str("根据id查询该订单出错"), status_code=status.HTTP_417_EXPECTATION_FAILED)
    return order_info

# 支付
# @router.post("/order_pay", tags=["orders"])
# async def order_pay(app:OrderParam):
#     try:
#         pay_url = order_service.order_pay(app)
#     except Exception as e:
#         logger.error("支付接口(order_pay):"+str(e))
#         return JSONResponse(content=str("支付出错"), status_code=status.HTTP_417_EXPECTATION_FAILED)
#     return pay_url

# 回调方法查询订单的支付状态
@router.post("/retracement", tags=["orders"])
async def call_back(result:str,sign:str):
    try:
        pay_url = order_service.call_back(result,sign)
    except Exception as e:
        logger.error("回调方法查询订单的支付状态接口(call_back):"+str(e))
        return JSONResponse(content=str("回调方法查询订单的支付状态出错"), status_code=status.HTTP_417_EXPECTATION_FAILED)
    return pay_url
