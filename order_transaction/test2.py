from util.rsa_util import RsaUtil
from util.snowflakeutil import IdWorker
import json
from datetime import datetime
import base64
if __name__ == '__main__':
    rsa_util = RsaUtil('./rsa_key/rsa_private_key.pem', './rsa_key/rsa_public_key.pem')
    data = json.dumps({
        "order_id":"1316645898964574208",
        "pay_mode":"alipay",
        "transtype":"0000",
        "total_money":"100",
        "notifyurl":"http://192.168.0.114:8001/order/findpaystatus",
        "order_ip":"192.168.0.114",
        "application_id":"1316618600274345984",
        "remark1":"",
        "remark2":"",
        "remark3": "",
        "remark4": "",
        "remark5": "",
        "brank_detail":[
            {
              "brank_number":"5654987213546",
              "brank_number_name":"招商银行",
              "order_detail":[
                  {
                      "category":"书籍",
                      "price":"50",
                      "good_id":"1",
                      "good_title":"钢铁是怎样炼成的",
                      "shop_id":"871034",
                      "shop_name":"笔趣阁",
                      "remark1":"",
                      "remark2":"",
                      "remark3":"",
                      "remark4":"",
                      "remark5":""
                  },
                  {
                      "category": "书籍",
                      "price": "50",
                      "good_id": "2",
                      "good_title": "时间简史",
                      "shop_id": "871034",
                      "shop_name": "笔趣阁",
                      "remark1": "",
                      "remark2": "",
                      "remark3": "",
                      "remark4": "",
                      "remark5": ""
                  }
              ]
            }
        ]
    })
    encrypt = rsa_util.public_long_encrypt(data)
    result = str(encrypt, encoding="utf8")
    sign = rsa_util.sign(result,"bbda32de628b08af4a480a517f5cf666")
    print(result)
    print(sign)
# if __name__ == '__main__':
#     rsa_ = RsaUtil('rsa_key/rsa_private_key.pem', 'rsa_key/rsa_public_key.pem')
#     # 对签名进行验证, md5(rsa(json)+key),与支付接口定义好的key
#     # 解密数据信息
#     result = "YOQbRwMg0HFw4Fcm_sltUMjPmKjFyEDFDO2rg_JyA8ZjWfdWI-OwA9cGlUxU_VYbGwqp67QeabwgdWMn1pberYZ9dzm2MaMj3OST-3bWuiAwXS30KW7HGLpsxFFgynLNb8kQb_V8FhSNrxxfW-6AeeFyhV_PeRSE83zFpABFpUgL7af6h3btF3PioJn8K_bL87UJ16K85DszZjFF3rrXGFAFuGgo3GiL7CNdvQszQvU2f4Vucu_5I1w1x6gaw2BVxXOzkIG1oABU1m2mOvbLL0_EkeY5eC2ity_wqRK4e-VpDxe-OVdlRjZg6HnBeZyoGyVfpfxwB_ND0-nkjGhzaghzjxsU7_DgwLLFOEuG_raoXC73ZqLKayWLcaDJUf5_2O3_KSFwraZ6zn660gGvmJ_kvo3baNVOUl0D2U9J4QcRVITEkLiq4Vwh70z0edF8pegYCCW2vHAGJFdt3c8XjvrOXZjzI7kA1hdGGQghPKZKbRNytHQ2__2pRkULlvp8XUn1y0j-3yDANbpmBu5PwPnoKlgudiltogSQfU6vIdc-UzwX6Nn6GY1IKLrNYhM5KMtKF5ofvNFfQg1Aw5QyAOM52SoMYddT78E-eKTGTXsKmzAEOTh2A12uvCEF-nsVSfx_nSM6AZXIs2R1P_vJkils4NzrLCIZiasA23US3_E="
#     mes = result.replace("-", "+").replace("_", "/") + "="
#     print(mes)
#     json_data = rsa_.private_long_decrypt(mes)
#     print(json_data)





