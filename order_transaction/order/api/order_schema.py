from pydantic import BaseModel
from pydantic.fields import Field
from datetime import datetime
from sqlalchemy import DECIMAL
from typing import List

class GetBrank(BaseModel):
    brank_id : str = Field(title='银行账户信息id', description='银行账户信息id') # 时间+
    sys_order_id : str = Field(title='sys_order_id', description='本系统为订单生成的id') # 时间+
    brank_number : str = Field(title='银行账户号', description='银行账户号') # 时间+
    brank_number_name : str = Field(title='银行账户名称', description='银行账户名称') # 时间+
    class Config:
        orm_mode = True

#子订单
class Order_Detail(BaseModel):
    order_detail_id:str = Field(title='子订单的id', description='子订单的id')
    sys_order_id:str = Field(title='本系统订单的id', description='本系统订单的id')
    price:float = Field(title='商品金额', description='商品金额')
    category:str = Field(title='商品类别', description='商品类别')
    good_id:int = Field(title='商品id', description='商品id')
    good_title:str = Field(title='商品标题', description='商品标题')
    shop_id:int = Field(None,title='店铺id', description='店铺id')
    shop_name:str = Field(None,title='店铺名称', description='店铺名称')
    bank_account_id:str = Field(title='银行账户信息id', description='银行账户信息id')
    remark1: str = Field(None,title='备注1', description='备注1')
    remark2: str = Field(None,title='备注2', description='备注2')
    remark3: str = Field(None,title='备注3', description='备注3')
    remark4: str = Field(None,title='备注4', description='备注4')
    remark5: str = Field(None,title='备注5', description='备注5')
    class Config:
        orm_mode = True

class Order(BaseModel):
    order_id: str = Field(title='订单号', description='调用方系统传入的订单号')
    pay_mode: str = Field(title='支付方式', description='1.微信支付 2.支付宝支付')
    transtype:str = Field(title='支付通道', description='0000:扫码支付')
    total_money:float = Field(title='订单总金额', description='订单总金额')
    qrcode_path:str = Field(None,title='二维码路径', description='二维码路径')
    order_ip: str = Field(title='订单的ip地址', description='订单的ip地址')
    notifyurl: str = Field(title='异步地址', description='异步地址')
    remark1: str = Field(None,title='备注1', description='备注1')
    remark2: str = Field(None,title='备注2', description='备注2')
    remark3: str = Field(None,title='备注3', description='备注3')
    remark4: str = Field(None,title='备注4', description='备注4')
    remark5: str = Field(None,title='备注5', description='备注5')
    order_details:List[Order_Detail] = Field(None,title='子订单信息', description='子订单信息')
    brank_order:List[GetBrank] = Field(None,title='子订单信息', description='子订单信息')
    class Config:
        orm_mode = True

class OrderParam(BaseModel):
    sign: str = Field(title='签名', description='签名')
    application_id: int = Field(title='系统id', description='系统id')
    result: str = Field(title='订单数据信息', description='使用json封装的订单数据信息')
    class Config:
        orm_mode = True

class GetOrder(Order):
    sys_order_id: str = Field(title='id', description='本系统为订单生成的id') # 时间+
    status: int = Field(title='订单状态', description='1.支付成功 2.支付失败')
    creat_time: datetime = Field(title='订单创建时间', description='订单创建时间')
    pay_time: datetime = Field(None,title='订单付款时间', description='订单付款时间')
    class Config:
        orm_mode = True

class Pre_Page_Order(BaseModel):
    items: List[GetOrder] = Field(title='订单信息集合', description='订单信息集合')
    total: int = Field(title='订单总条数', description='订单总条数')
    class Config:
        orm_mode = True