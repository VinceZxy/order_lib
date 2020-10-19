import qrcode

def creat_qrcode_util(content,path):
    # 生成二维码实例，设置大小和边框
    qr = qrcode.QRCode(box_size=10, border=2)
    # 添加二维码的显示信息
    # content = "http://192.168.0.114:8000/api/test"
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image()
    # 保存二维码
    img.save(path)

