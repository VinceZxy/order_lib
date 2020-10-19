from fastapi import status
from util.rsa_util import RsaUtil
from fastapi.responses import JSONResponse
from logger import logger
from set_path_config import *
from application.dao import application_dao
import json
#用于其他系统的数据处理
def DockingVerification(app):
    #     # 对加密数据进行处理
    rsa_data = app.result
    application_id = app.application_id
    # 读取公钥,私钥
    # 实例化公钥，私钥
    logger.info("(1).实例化本系统的公钥，私钥")
    rsa_util = RsaUtil('rsa_key/rsa_private_key.pem', 'rsa_key/rsa_public_key.pem')
    # 解密数据信息
    json_data = rsa_util.private_long_decrypt(rsa_data)
    logger.info("(2).解密数据信息:" + str(json_data))
    # 对签名进行验证, md5(rsa(json)+key),key从数据库中查询，这个系统的key
    application_id = application_dao.get_application_bysysid(application_id)
    logger.info("(3).查询系统的key" + str(application_id.key))
    sys_sign = rsa_util.sign(app.result, application_id.key)
    logger.info("(3.1).签名信息:" + str(sys_sign))
    if sys_sign != app.sign:
        logger.error("(3.1).签名有误:系统签名:" + str(sys_sign) + ",用户签名:" + str(app.sign))
        return JSONResponse(content=str("签名不一致"), status_code=status.HTTP_417_EXPECTATION_FAILED)
    # 对json数据做处理
    order_dict = json.loads(json_data)
    return order_dict

#用于支付交易前台数据处理
def Frond_DockingVerification(app):
    #     # 对加密数据进行处理
    rsa_data = app.result
    # 读取公钥,私钥
    # 实例化公钥，私钥
    logger.info("(1).实例化本系统的公钥，私钥")
    rsa_util = RsaUtil('rsa_key/rsa_private_key.pem', 'rsa_key/rsa_public_key.pem')
    # 解密数据信息
    json_data = rsa_util.private_long_decrypt(rsa_data)
    logger.info("(2).解密数据信息:" + str(json_data))
    # 对签名进行验证, md5(rsa(json)+key),与订单交易系统前台定义好的key
    # key = os.environ.get("Frond_Key")
    # sys_sign = rsa_util.sign(app.result,key)
    # logger.info("(3).签名信息:" + str(sys_sign))
    # if sys_sign != app.sign:
    #     logger.error("(3.1).签名有误:系统签名:" + str(sys_sign) + ",用户签名:" + str(app.sign))
    #     return JSONResponse(str("签名不一致"), status_code=status.HTTP_417_EXPECTATION_FAILED)
    # 对json数据做处理
    order_dict = json.loads(json_data)
    return order_dict