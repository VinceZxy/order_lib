from pydantic import BaseModel
from pydantic.fields import Field
from datetime import datetime
from typing import List

class Application(BaseModel):
    name: str = Field(title='系统名称', description='系统名称')
    public_key: str = Field(title='公钥', description='公钥用来对数据进行加密')
    key: str = Field(title='key', description='调用方与被调用方约定的值')
    account: str = Field(title='系统账户', description='系统账户')
    email:str = Field(title='系统的邮箱',description='系统的邮箱')
    code:str = Field(title='系统使用的编码',description='系统使用的编码')
    admin_name:str = Field(title='系统管理员姓名',description='系统管理员姓名')
    admin_phone:str = Field(title='系统管理员手机号',description='系统管理员手机号',max_length=11,min_length=11)
    ip:str = Field(title='系统的ip',description='系统的ip')
    remark1:str = Field(None,title='备注1',description='备注1')
    remark2:str = Field(None,title='备注2',description='备注2')
    remark3:str = Field(None,title='备注3',description='备注3')
    remark4:str = Field(None,title='备注4',description='备注4')
    remark5:str = Field(None,title='备注5',description='备注5')
    class Config:
        orm_mode = True

class DeleteApplication(Application):
    sys_id:str = Field(title='系统id', description='系统id')
    delete_time: datetime = Field(title='系统删除时间', description='系统删除时间')
    class Config:
        orm_mode = True

class Pre_Page_Application(BaseModel):
    items:List[Application]= Field(title='系统信息', description='系统信息')
    total:int= Field(title='系统总条数', description='系统总条数')
    class Config:
        orm_mode = True