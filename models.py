#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column # 创建字段用
from sqlalchemy import Integer, String, DECIMAL # 导入对应的字段类型
from sqlalchemy import ForeignKey  #导入外键
from sqlalchemy import create_engine # 配置引擎
from sqlalchemy.orm import  relationship  #创建关系


# 使用基类模型进行创建新的类,这个新的类就有了与表对应的结构映射关系
Base = declarative_base()
# 生成自己的类,类名就是表名
#需求
class Requirement(Base):
    __tablename__='requirement'
    id = Column(Integer, primary_key=True)
    title = Column('title',String(255),nullable=False)
    defenses = relationship("Defense",back_populates="requirement",lazy="dynamic")

    def __repr__(self):
        return self.title

#防御
class Defense(Base):
    __tablename__='defense'
    id = Column(Integer, primary_key=True)
    title = Column('title',String(255),nullable=False)
    requirement_id = Column(Integer,ForeignKey("requirement.id"),nullable=False)
    requirement = relationship("Requirement",order_by="Requirement.id",back_populates="defenses")
    securityActivities = relationship("SecurityActivities",back_populates="defense",lazy="dynamic")

    def __repr__(self):
        return self.title

    def getInfo(self):
        return self.requirement.title+"--"+self.title

#方法
class SecurityActivities(Base):
    __tablename__='securityActivities'
    id = Column(Integer, primary_key=True)
    title = Column('title',String(255),nullable=False)
    cost = Column('cost',Integer,nullable=False) #花费金额
    maintenance = Column('maintenance',Integer,nullable=False) #维护等级难度
    efficiency = Column('efficiency',Integer,nullable=False) #有效程度
    defense_id = Column(Integer,ForeignKey("defense.id"),nullable=False)
    defense = relationship("Defense",order_by="Defense.id",back_populates="securityActivities")

    def __repr__(self):
        return self.title

    def getInfo(self):
        return [self.defense.requirement.title,self.defense.title,self.title,
                self.cost,self.maintenance,self.efficiency]

    def getMess(self):
        return [self.id,self.title,self.cost,self.maintenance,self.efficiency]



# 连接数据库并建立表格
def link_mysql():
    # 配置引擎
    engine = create_engine('mysql+pymysql://root:password@127.0.0.1:3306/test')
    # 利用基类创建表
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    link_mysql()
