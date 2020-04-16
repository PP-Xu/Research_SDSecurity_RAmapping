
# -*- coding:utf-8 -*-


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column 
from sqlalchemy import Integer, String, DECIMAL 
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import  relationship 


# the Base is uesd to creat other new classes with mapping relations
Base = declarative_base()
# creat new class

#requirements
class Requirement(Base):
    __tablename__='requirement'
    id = Column(Integer, primary_key=True)
    title = Column('title',String(255),nullable=False)
    defenses = relationship("Defense",back_populates="requirement",lazy="dynamic")

    def __repr__(self):
        return self.title

#Defense
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

#Activities
class SecurityActivities(Base):
    __tablename__='securityActivities'
    id = Column(Integer, primary_key=True)
    title = Column('title',String(255),nullable=False)
    
    cost = Column('cost',Integer,nullable=False) 
    maintenance = Column('maintenance',Integer,nullable=False)
    efficiency = Column('efficiency',Integer,nullable=False)
    defense_id = Column(Integer,ForeignKey("defense.id"),nullable=False)
    defense = relationship("Defense",order_by="Defense.id",back_populates="securityActivities")

    def __repr__(self):
        return self.title

    def getInfo(self):
        return [self.defense.requirement.title,self.defense.title,self.title,
                self.cost,self.maintenance,self.efficiency]

    def getMess(self):
        return [self.id,self.title,self.cost,self.maintenance,self.efficiency]



# connect the database
def link_mysql():
    # config the engine
    engine = create_engine('mysql+pymysql://root:password@127.0.0.1:3306/test')
    # cerat tables
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    link_mysql()
