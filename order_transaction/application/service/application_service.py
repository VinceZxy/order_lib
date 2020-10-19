from logger import logger
from util.snowflakeutil import IdWorker
from application.dao import application_dao
def add_application(app):
    sys_id = str(IdWorker(3, 4).get_id())
    mes = application_dao.add_application(app,sys_id)
    return mes

def get_applications(page,pre_page,is_order_by,filter_mes):
    pagination = application_dao.get_applications(page,pre_page,is_order_by,filter_mes)
    return pagination

def get_application_bysysid(sys_id):
    application_info = application_dao.get_application_bysysid(sys_id)
    return application_info

def updata_applications(sys_id,app):
    application_dao.updata_applications(sys_id,app)

def del_applications(sys_id):
    application_dao.del_applications(sys_id)