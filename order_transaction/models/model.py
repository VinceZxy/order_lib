from sqlalchemy import Column, String, Integer, DateTime,Date,ForeignKey,Table,BIGINT,DECIMAL ,func
from sqlalchemy.orm import relationship
from sqlalchemy_pagination import paginate
from config.dataBase.data_base_client import Base

class Brank_Account(Base):
    __tablename__ = 't_brank_account'
    brank_id = Column(String(30), primary_key=True)
    sys_order_id = Column(String(30),ForeignKey("t_order.sys_order_id"))
    brank_number = Column(String(50))
    brank_number_name = Column(String(50))

class Application(Base):
    __tablename__ = 't_application'
    sys_id = Column(String(30), primary_key=True)
    name = Column(String(20))
    public_key = Column(String(255))
    key = Column(String(255))
    account = Column(String(50))
    email = Column(String(50))
    code = Column(String(10))
    admin_name = Column(String(50))
    admin_phone = Column(String(20))
    ip = Column(String(255))
    register_time = Column(DateTime)
    update_time = Column(DateTime)
    delete_time = Column(DateTime)
    status = Column(BIGINT)
    is_delete = Column(BIGINT)
    remark1 = Column(String(255))
    remark2 = Column(String(255))
    remark3 = Column(String(255))
    remark4 = Column(String(255))
    remark5 = Column(String(255))

class Order(Base):
    __tablename__ = 't_order'
    sys_order_id = Column(String(30), primary_key=True)
    order_id = Column(String(255))
    pay_mode = Column(String(255))
    transtype = Column(String(255))
    total_money = Column(DECIMAL)
    qrcode_path = Column(String(255))
    order_ip = Column(String(20))
    application_id = Column(String(30),ForeignKey("t_application.sys_id"))
    notifyurl = Column(String(255))
    status = Column(BIGINT)
    creat_time = Column(DateTime)
    pay_time = Column(DateTime)
    remark1 = Column(String(255))
    remark2 = Column(String(255))
    remark3 = Column(String(255))
    remark4 = Column(String(255))
    remark5 = Column(String(255))
    order_details = relationship("OrderDetail", lazy="joined")
    brank_order = relationship("Brank_Account", lazy="joined")

class OrderDetail(Base):
    __tablename__ = 't_order_detail'
    order_detail_id = Column(String(30), primary_key=True)
    sys_order_id = Column(String(30),ForeignKey("t_order.sys_order_id"))
    price = Column(DECIMAL)
    category = Column(String(255))
    good_id = Column(Integer)
    good_title = Column(String(50))
    shop_id = Column(Integer)
    shop_name = Column(String(50))
    bank_account_id = Column(String(30),ForeignKey("t_brank_account.brank_id"))
    remark1 = Column(String(255))
    remark2 = Column(String(255))
    remark3 = Column(String(255))
    remark4 = Column(String(255))
    remark5 = Column(String(255))


