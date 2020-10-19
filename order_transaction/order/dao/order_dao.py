from models import model
from datetime import datetime
from logger import logger
from models.model import paginate
from util import snowflakeutil
from config.dataBase.data_base_client import engine,DbLife
model.Base.metadata.create_all(bind=engine)

def add_order(order_dict,sys_id,qrcode_path):
    try:
        with DbLife() as db:
            #添加主订单信息
            logger.info("(4)添加订单")
            order_data = db.query(model.Order).filter(model.Order.order_id==order_dict["order_id"]).first()
            if order_data != None:
                logger.info("(error)不能添加同一订单")
                return "不能添加同一订单"
            order_init = model.Order(sys_order_id=sys_id,
                        order_id=order_dict["order_id"],
                        pay_mode=order_dict["pay_mode"],
                        transtype=order_dict["transtype"],
                        total_money=order_dict["total_money"],
                        qrcode_path=qrcode_path,
                        order_ip=order_dict["order_ip"],
                        application_id=order_dict["application_id"],
                        notifyurl=order_dict["notifyurl"],
                        status=3,
                        creat_time=datetime.now(),
                        remark1=order_dict["remark1"],
                        remark2=order_dict["remark2"],
                        remark3=order_dict["remark3"],
                        remark4=order_dict["remark4"],
                        remark5=order_dict["remark5"],
                       )
            db.add(order_init)
            db.begin_nested() #创建一个子嵌套事务，第一个commit只是将子事务的数据托管到父事务，并未提交到数据库,如果下面错误进行事务回滚
            db.commit()
            # 添加订单下银行账户信息
            logger.info("(5)添加订单下银行账户信息")
            param_brank_detail = order_dict["brank_detail"]
            for brank_detail in param_brank_detail:
                bank_init= model.Brank_Account(brank_id=str(snowflakeutil.IdWorker(5,6).get_id()),
                                    sys_order_id = order_init.sys_order_id,
                                    brank_number =brank_detail["brank_number"],
                                    brank_number_name=brank_detail["brank_number_name"])
                db.add(bank_init)
                db.begin_nested()  # 创建一个子嵌套事务，第一个commit只是将子事务的数据托管到父事务，并未提交到数据库,如果下面错误进行事务回滚
                db.commit()
                # 添加子订单信息
                logger.info("(6)添加子订单信息")
                param_order_details = brank_detail["order_detail"]
                order_detail_ids = []
                for order_detail in param_order_details:
                    # 生成本系统的子订单id  （采用主订单id+生成雪花算法的后六位）
                    temp = str(snowflakeutil.IdWorker(3, 4).get_id())
                    sys_order_detail_id = sys_id + "-" + temp[-6:]
                    order_detail_data= model.OrderDetail(order_detail_id=sys_order_detail_id,
                                      sys_order_id=order_init.sys_order_id,
                                      category=order_detail["category"],
                                      price=order_detail["price"],
                                      good_id=order_detail["good_id"],
                                      good_title=order_detail["good_title"],
                                      shop_id=order_detail["shop_id"],
                                      shop_name=order_detail["shop_name"],
                                      bank_account_id=bank_init.brank_id
                                      )
                    db.add(order_detail_data)
                    db.commit()
                    order_detail_ids.append(order_detail_data.order_detail_id)
            logger.info("(7)添加订单成功")
            dict_info = {"sys_order_id":order_init.sys_order_id,"order_detail_ids":order_detail_ids,"creat_time":order_init.creat_time}
            return dict_info
    except  Exception as e:
        db.rollback()
        logger.error("(error)添加失败，事务回滚，错误信息:"+str(e))
        return "添加失败"

def get_orders(page,pre_page,is_order_by,filter_mes):
    with DbLife() as db:
        if is_order_by != None:
            pagination = paginate(
                db.query(model.Order).order_by(is_order_by), page,
                pre_page)
        if is_order_by == None:
            pagination = paginate(db.query(model.Order), page, pre_page)
        return pagination


def get_order_id(application_id,order_id):
    with DbLife() as db:
        order_info = db.query(model.Order).filter(model.Order.application_id==application_id,model.Order.order_id==order_id).first()
    return order_info

def call_back_success(sys_order_id,timestamp):
    with DbLife() as db:
        order_info = db.query(model.Order).filter(model.Order.sys_order_id==sys_order_id).first()
        setattr(order_info,"status",1)
        setattr(order_info, "pay_time",timestamp)
        db.commit()
        db.refresh(order_info)
    return order_info

def call_back_error(sys_order_id):
    with DbLife() as db:
        order_info = db.query(model.Order).filter(model.Order.sys_order_id==sys_order_id).first()
        setattr(order_info,"status",2)
        db.commit()
        db.refresh(order_info)
    return order_info

def delete_error_order(order_id,application_id):
    with DbLife() as db:
        order_info = db.query(model.Order).filter(model.Order.order_id == order_id,
                                                  model.Order.application_id==application_id).first()
        brank_account = db.query(model.Brank_Account).filter(model.Brank_Account.sys_order_id == order_info.sys_order_id).first()
        order_details = db.query(model.OrderDetail).filter(model.OrderDetail.sys_order_id == order_info.sys_order_id).all()
        db.delete(order_info)
        logger.info("(error).删除订单信息(order_info)是:" + order_info.sys_order_id)
        db.delete(brank_account)
        logger.info("(error).删除银行账户信息(brank_account)是:" + brank_account.brank_id)
        for order_detail in order_details:
            db.delete(order_detail)
            logger.info("(error).删除子订单信息(order_detail)是:" + order_detail.order_detail_id)
        db.commit()
        db.flush()
