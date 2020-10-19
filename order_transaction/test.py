from util.rsa_util import RsaUtil
from util.snowflakeutil import IdWorker
import json
from datetime import datetime
import base64
# if __name__ == '__main__':
#     rsa_util = RsaUtil('./rsa_key/rsa_private_key.pem', './rsa_key/rsa_public_key.pem')
#     #  "sys_order_id":"",
#     data = json.dumps({
#         "order_id":"1316645898964574208"
#     })
#     encrypt = rsa_util.public_long_encrypt(data)
#     result = str(encrypt, encoding="utf8")
#     sign = rsa_util.sign(result,"bbda32de628b08af4a480a517f5cf666")
#     print(result)
#     print(sign)
if __name__ == '__main__':
    rsa_ = RsaUtil('rsa_key/rsa_private_key.pem', 'rsa_key/rsa_public_key.pem')
    # 对签名进行验证, md5(rsa(json)+key),与支付接口定义好的key
    # 解密数据信息
    result = "dN5iXbIBkSubcvZ6kTvodaD5u5GAe8Y1Di_3tLrN5S82ZLT87dIF1C2gQ_G4r8yr1O0b2AqvS5Rz_9vY3ezxwleYajHTHeQVoD9c1HCqtTedzGaDh2XNqZu_9YBgunr0QhKcBkW1y8w6IAvXVrWNh2pKyo4-qvJTYYDFLAnqx4QX8XAyiEOJtPKfSXOYXogoV4dn3zvlABGdxmhDB40TFAl1e64uN1q6ne-92RrhsJFU1Kw2H_An3kSkYPWJBQ8COhTn_Cs7WHQD36-l7bMRANcAqNc6Sn8OMNJYeASVz4l1ceU-BMSVZWfvY4hARuEGv6F6XM1H5ay21rN0lecqJG-nhF9GeeiGWH3RWabvEZ_m6m6kbafVGXpaRLM6npAvK3o-TdEh-OLe_TqHf1I-gNcGZpDCh5jrbmcQOVP83lX-K7FW8clS7jdSpwpz9bbH4IdsyDGHfNeLI0Xf1DTZ2dUe8sz-xVrqnPndbOf9x4cVhuwAKXt-3V-TxZx1U_UmYVm7oJkXNYcaWT_EYoUPh4gzqgeY61cANqL4Lp5LPKTXjepnf4D3F1DLATJ8z4cItQBuewcHcLqeF4FGIn-gaH-95TUmeItsNWaEiSJxO3ojhi00aQ0r-YSfoB1-E4Xp2kGAytNqptNErQSE9rD4_ltL5v0LZWpUamolrYPgAyw="
    mes = result.replace("-", "+").replace("_", "/") + "="
    print(mes)
    json_data = rsa_.private_long_decrypt(mes)
    print(json_data)





