from fastapi import status
from util import rsa_util,snowflakeutil,qrcode_utils, sys_rsa_util
from common import docking_util,sendRsaData
from fastapi.responses import JSONResponse
from logger import logger
from set_path_config import *
from order.dao import order_dao
from urllib import parse
import requests
from application.dao import application_dao
import json

def add_order(app):
    logger.info("--------------------------添加订单信息-----------------------------")
    # 验证是否能对接,解密订单信息
    order_dict = docking_util.DockingVerification(app)
    #生成本系统的订单id可以作为二维码名称/path
    sys_order_id = str(snowflakeutil.IdWorker(1,2).get_id())
    qrcode_path = "static/"+sys_order_id + ".png"
    # 将订单填入数据库
    # 如果传入的子订单的金额加起来与主订单总金额不相等
    param_brank_details = order_dict["brank_detail"]
    sum_good_price = 0
    for brank_detail in param_brank_details:
        for order_detail in brank_detail["order_detail"]:
            sum_good_price += float(order_detail["price"])
    if sum_good_price != float(order_dict["total_money"]):
        logger.error("(erro):子订单价格总和与主订单金额不符合")
        return "子订单价格总和与主订单金额不符合"
    mes = order_dao.add_order(order_dict,sys_order_id,qrcode_path)
    if mes != "添加失败":
        if mes == "不能添加同一订单":
            mes_info = {"info": "不能添加同一订单"}
            rsa_data = sendRsaData.rsa_data(order_dict["application_id"],mes_info)
            return rsa_data
        logger.info("--------------------------调用支付接口-----------------------------")
        pay_url= order_pay(order_dict,mes["order_detail_ids"],mes["creat_time"],order_dict["application_id"])
            # 使用系统的公钥加密数据发回到回调地址
        mes_info = {"sys_order_id":mes["sys_order_id"],"data":pay_url}
        rsa_data = sendRsaData.rsa_data(order_dict["application_id"],mes_info)
        if pay_url.startswith("http://pay.52yaxin.com"):
            # 生成订单二维码
            qrcode_utils.creat_qrcode_util("https://192.168.0.114:/#/orders/" + sys_order_id, qrcode_path)
            logger.info("(14).生成二维码订单:" + qrcode_path)
        return rsa_data
    mes_info = {"info": "支付失败"}
    rsa_data = sendRsaData.rsa_data(order_dict["application_id"], mes_info)
    return rsa_data


def get_orders(page,pre_page,is_order_by,filter_mes):
    pagination = order_dao.get_orders(page,pre_page,is_order_by,filter_mes)
    return pagination


def get_order_id(app):
    order_dict = docking_util.Frond_DockingVerification(app)
    order_id = order_dict["order_id"]
    param_application_id = app.application_id
    order_info = order_dao.get_order_id(param_application_id,order_id)
    if order_info != None:
        init_order_dict = {"sys_order_id": order_info.sys_order_id,
                           "order_id": order_info.order_id,
                           "pay_mode": order_info.pay_mode,
                           "transtype": order_info.transtype,
                           "total_money": order_info.total_money,
                           "qrcode_path": order_info.qrcode_path,
                           "order_ip": order_info.order_ip,
                           "application_id": order_info.application_id,
                           "notifyurl": order_info.notifyurl,
                           "status": order_info.status,
                           "creat_time": order_info.creat_time,
                           "pay_time": order_info.pay_time}
        rsa_success_data = sendRsaData.Frond_rsa_data(init_order_dict)
        return rsa_success_data
    mes_info = {"data":"", "info": "未查询到订单信息"}
    rsa_error_data = sendRsaData.Frond_rsa_data(mes_info)
    return rsa_error_data
# 一马陷足淤泥内，老畜生怎样出蹄  一人跩绳马蹄上,王公子这样答题，
# 小马不服人上坐，小鞭一出应声啼，此啼皆因不服气，
def order_pay(order_dict,order_detail_ids,creat_time,application_id):
    url = 'http://47.95.254.69:8080/payinterface/index.do'
    #验证是否能对接,解密订单信息  3
    # order_dict = docking_util.Frond_DockingVerification(app)
    branklist = []
    orderlist = []
    for brank_info in order_dict["brank_detail"]:
        for index,order_info in enumerate(brank_info["order_detail"]):
            order_data = {
                    "title": order_info["good_title"],
                    "shopid": order_info["good_id"],
                    "categoryname": order_info["category"],
                    "price": int(float(order_info["price"])*100),
                    "suborderid": order_detail_ids[index],
                    "remark1": "备注1",
                    "remark2": "备注2"
            }
            orderlist.append(order_data)
    for brank_info in order_dict["brank_detail"]:
        brank_data = {
            "banknumber": brank_info["brank_number"],
            "numbername": brank_info["brank_number_name"],
            "remark1": "备注1",
            "remark2": "备注2",
            "detaillist": orderlist
        }
        branklist.append(brank_data)
    data = json.dumps({
         "ordernumber":order_dict["order_id"],
         "ordertime":str(creat_time),
         "merid":os.environ.get("MERID"),
         "paytype":"alipay",
         "transtype":"0000",
         "signmethon":"RSA",
         "charset":"utf8",
         "notifyurl":os.environ.get("NOTIFYURL"),
         "backurl": os.environ.get("BACKURL"),
         "customerip": "192.168.0.114",
         "amount":int(float(order_dict["total_money"])*100),
         "remark1": "备⽤1",
         "remark2": "备⽤2",
         "remark3": "备⽤3",
         "remark4": "备⽤4",
         "remark5": "备⽤5",
         "remark6": "备⽤6 ",
         "remark7": "备⽤7",
         "remark8": "备⽤8",
         "remark9": "备⽤9",
         "remark10": "备⽤10",
         "remark11": "备⽤11",
         "remark12": "备⽤12",
         "datalist":branklist
    })
    logger.info("(9).拼接支付接口的json字符串:"+data)
    logger.info("(10).实例化支付系统的公钥，私钥")
    rsa_ = rsa_util.RsaUtil('rsa_key/orderPay_private_key.pem', 'rsa_key/orderPay_public_key.pem')
    logger.info("(11).对json参数进行加密")
    encrypt = rsa_.public_long_encrypt(data)  # 对json参数进行加密
    result = str(encrypt, encoding="utf8")
    key = os.environ.get("MER_KEY")
    sign = rsa_.sign(result,key)
    logger.info("(12).生成签名:"+sign)
    HEADERS = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
    FormData = {"result": result, "sign": sign.upper(), "merid": "1CC92CF3C585AF4DE2609EFFE69A21CD"}
    data = parse.urlencode(FormData)
    content = requests.post(url=url, headers=HEADERS, data=data).text
    if content.startswith("http://pay.52yaxin.com"):
        logger.info("(13).调用支付接口成功返回支付地址:"+content)
        return content
    #没有调用成功支付接口需要删除订单信息
    logger.info("(error).没有调用成功支付接口需要删除订单信息:")
    order_dao.delete_error_order(order_dict["order_id"],application_id)
    return content

def call_back(result,sign):
    # 对加密数据进行处理
    # 读取公钥,私钥
    # 实例化公钥，私钥
    logger.info("(1).实例化支付接口的公钥，私钥")
    rsa_ = rsa_util.RsaUtil('rsa_key/rsa_private_key.pem', 'rsa_key/rsa_public_key.pem')
    logger.info("(2).对签名进行验证签名信息:" + str(sign))
    # 对签名进行验证, md5(rsa(json)+key),与支付接口定义好的key
    key = os.environ.get("MER_KEY")
    sys_sign = rsa_.sign(result, key)
    if sys_sign != sign:
        logger.error("(2.1).签名有误:系统签名:" + str(sys_sign) + ",支付接口签名:" + str(sign))
        return JSONResponse(str("签名不一致"), status_code=status.HTTP_417_EXPECTATION_FAILED)
    # 解密数据信息
    json_data = rsa_.private_long_decrypt(result)
    logger.info("(3).解密数据信息:" + str(json_data))
    # 对json数据做处理
    order_dict = json.loads(json_data)
    logger.info("(4).修改订单的状态")
    if order_dict["status"] == "0":
        #支付成功
        #用本系统公钥加密发送给回调地址的接口, 返回的信息status = 1
        #支付成功
        # 修改订单的状态改为支付成功
        logger.info("(4.1).修改订单的状态改为支付成功")
        order_info = order_dao.call_back_success(order_dict["ordernumber"],order_dict["timestamp"])
    else:
        # 支付失败
        # 修改订单的状态改为支付失败status = 2
        logger.info("(4.2).解密数据信息:" + str(json_data))
        order_info = order_dao.call_back_error(order_dict["ordernumber"])
    init_order_dict = {"sys_order_id": order_info.sys_order_id,
                       "order_id": order_info.order_id,
                       "pay_mode": order_info.pay_mode,
                       "transtype": order_info.transtype,
                       "total_money": order_info.total_money,
                       "qrcode_path": order_info.qrcode_path,
                       "order_ip": order_info.order_ip,
                       "application_id": order_info.application_id,
                       "notifyurl": order_info.notifyurl,
                       "status": order_info.status,
                       "creat_time": order_info.creat_time,
                       "pay_time": order_info.pay_time}
    #使用系统的公钥加密数据发回到回调地址
    sendRsaData.send_rsa_data(order_dict["ordernumber"],init_order_dict)


