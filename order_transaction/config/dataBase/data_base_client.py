# 导入SQLAlchemy部分
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from set_path_config import *
# 为SQLAlchemy创建数据库
# 数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名
from sqlalchemy.util import decorator

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://"+os.environ.get("MYSQL_USERNAME")+":"+os.environ.get("MYSQL_PASSWORD")+"@"+os.environ.get("IP")+":3306/"+os.environ.get("MYSQL_DATABASE")+""
# 相对路径下创建sqlite
# engine = create_engine('sqlite:///signup.db')
# 绝对路径形式创建sqlite
# engine = create_engine('sqlite:////absolute/path/to/foo.db')
# PostgreSQL
# engine = create_engine('postgresql://root:123456@localhost/fastapi')
# oracle
# db = create_engine('oracle://root:123456@localhost:1521/fastapi')
# SQLserver
# create_engine('mssql+pymssql://Login:Password@Servername/DBname',echo=True)    #初始化数据库连接
# 创建一个SQLAlchemy“引擎”
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_size=16,
    pool_pre_ping=True,
    encoding='utf-8'
)
# SessionLocal该类的每个实例将是一个数据库会话。该类本身还不是数据库会话。
# 一旦我们创建了SessionLocal该类的实例，该实例将成为实际的数据库会话。
# 我们SessionLocal将其命名为有别于Session我们从SQLAlchemy导入的名称。
# 稍后我们将使用Session（从SQLAlchemy导入的一种）。
# 要创建SessionLocal类，请使用函数sessionmaker：

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 现在，我们将使用declarative_base()返回类的函数。
# 稍后，我们将从该类继承以创建每个数据库模型或类（ORM模型）：
Base = declarative_base()


class DbLife():
    def __init__(self):
        self.db_session = SessionLocal()  # 成员变量

    def __enter__(self):
        # 获得并返回session
        return self.db_session

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 释放session
        self.db_session.close()
