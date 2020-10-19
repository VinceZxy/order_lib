from util import sys_rsa_util
from logger import logger
from set_path_config import *
from application.dao import application_dao
import json
import requests
import datetime
import dateutil.parser
import decimal

from urllib import parse
def send_rsa_data(sys_order_id,mes_info):
    # 查询这个订单下的系统公钥
    logger.info("-----------------------将数据rsa加密发送给调用方系统-------------------------------")
    logger.info("(1).查询这个订单下的系统公钥")
    application_info = application_dao.order_pay_find_pubKey_byOrderId(sys_order_id)
    sys_rsa = sys_rsa_util.RsaUtil(application_info.public_key, "")
    data = json.dumps(mes_info, cls=MyJSONEncoder)
    send_result = sys_rsa.public_long_encrypt(data)
    logger.info("(2).对信息数据进行加密")
    send_sign = sys_rsa.sign(data, application_info.key)
    logger.info("(3).生成签名")
    url = mes_info["notifyurl"]
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    FormData = {"result": send_result, "sign": send_sign.upper()}
    data = parse.urlencode(FormData)
    requests.post(url=url, headers=HEADERS, data=data)
    logger.info("(4).将数据发送给回调地址:"+mes_info["notifyurl"])

def rsa_data(application_id,mes_info):
    # 查询这个订单下的系统公钥
    logger.info("-----------------------将数据rsa加密返回-------------------------------")
    logger.info("(1).查询这个订单下的系统公钥")
    application_info = application_dao.find_pubKey_byOrderId(application_id)
    sys_rsa = sys_rsa_util.RsaUtil(application_info.public_key,"")
    data = json.dumps(mes_info, cls=MyJSONEncoder)
    rsa_data = sys_rsa.public_long_encrypt(data)
    logger.info("(2).对信息数据进行加密")
    return rsa_data

def Frond_rsa_data(mes_info):
    # 查询这个订单下的系统公钥
    logger.info("-----------------------将数据rsa加密返回-------------------------------")
    key = os.environ.get("Frond_Public_KEY")
    sys_rsa = sys_rsa_util.RsaUtil(key,"")
    data = json.dumps(mes_info, cls=MyJSONEncoder)
    rsa_data = sys_rsa.public_long_encrypt(data)
    logger.info("(2).对信息数据进行加密")
    return rsa_data

CONVERTERS = {
    'datetime': dateutil.parser.parse,
    'decimal': decimal.Decimal,
}
class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.datetime,)):
            return obj.isoformat()
        elif isinstance(obj, (decimal.Decimal,)):
            return str(obj)
        else:
            return super().default(obj)