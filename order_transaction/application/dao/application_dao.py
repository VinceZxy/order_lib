from models import model
from models.model import func,paginate
from datetime import datetime
from logger import logger
from config.dataBase.data_base_client import engine,DbLife
model.Base.metadata.create_all(bind=engine)

def add_application(app,sys_id):
    try:
        with DbLife() as db:
            application =model.Application(sys_id=sys_id,
                              name=app.name,
                              public_key=app.public_key,
                              key=app.key,
                              account=app.account,
                              email=app.email,
                              code=app.code,
                              admin_name=app.admin_name,
                              admin_phone=app.admin_phone,
                              ip=app.ip,
                              register_time=datetime.now(),
                              is_delete=0)
            db.add(application)
            db.commit()
            return "添加成功"
    except  Exception as e:
        db.rollback()
        logger.error("(error)添加失败，事务回滚，错误信息:"+str(e))
        return "添加失败，事务回滚"

def get_applications(page,pre_page,is_order_by,filter_mes):
    with DbLife() as db:
        if is_order_by != None:
            pagination = paginate(db.query(model.Application).filter(model.Application.is_delete!=1).order_by(is_order_by),page, pre_page)
        if is_order_by == None:
            pagination = paginate(db.query(model.Application).filter(model.Application.is_delete!=1), page, pre_page)
        return pagination

def get_application_bysysid(sys_id):
    with DbLife() as db:
       application_info = db.query(model.Application).filter(model.Application.sys_id==sys_id,model.Application.is_delete!=1).first()
       return application_info

def updata_applications(sys_id,app):
    with DbLife() as db:
       application_info = db.query(model.Application).filter(model.Application.sys_id==sys_id,model.Application.is_delete!=1).first()
       if application_info != None:
           setattr(application_info, "name",app.name)
           setattr(application_info, "public_key", app.public_key)
           setattr(application_info, "key", app.key)
           setattr(application_info, "account", app.account)
           setattr(application_info, "email", app.email)
           setattr(application_info, "admin_name", app.admin_name)
           setattr(application_info, "admin_phone", app.admin_phone)
           setattr(application_info, "update_time", datetime.now())
           db.commit()
           db.flush(application_info)

def del_applications(sys_id):
    with DbLife() as db:
        application_info = db.query(model.Application).filter(model.Application.sys_id == sys_id,
                                                              model.Application.is_delete != 1).first()
        if application_info != None:
            setattr(application_info, "is_delete",1)
            setattr(application_info, "delete_time",datetime.now())
            db.commit()
            db.flush(application_info)

def find_pubKey_byOrderId(application_id):
    with DbLife() as db:
        application_info = db.query(model.Application).filter(model.Application.sys_id == application_id,
                                                            model.Application.is_delete != 1).first()
        return application_info

def order_pay_find_pubKey_byOrderId(sys_order_id):
    with DbLife() as db:
        order = db.query(model.Order).filter(model.Order.sys_order_id==sys_order_id).first()
        application_info = db.query(model.Application).filter(model.Application.sys_id == order.application_id,
                                                            model.Application.is_delete != 1).first()
        return application_info