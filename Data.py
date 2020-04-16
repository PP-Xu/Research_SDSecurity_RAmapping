#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from models import *

class Models_Data:
    def __init__(self):
        self.engine = create_engine('mysql+pymysql://root:password@127.0.0.1:3306/test')
        self.Session_class = sessionmaker(bind=self.engine)
        self.session = self.Session_class()
        self.cols=["cost","maintenance","efficiency"]

    def get_Requirements(self):
        requirements = self.session.query(Requirement).all()
        return requirements

    def get_OtherData(self,ids,type):
        if type>=2:
            return self.session.query(SecurityActivities).filter(SecurityActivities.defense_id.in_(ids)).all()
        defenses = self.session.query(Defense).filter(Defense.requirement_id.in_(ids)).all()
        # securityActivities = self.session.query(SecurityActivities).filter(SecurityActivities.defense_id.in_(ids)).all()
        return defenses

    def get_SecurityActivities(self,ids,col="",reverse=True):
        ms = self.session.query(SecurityActivities).filter(SecurityActivities.id.in_(ids))
        if col in self.cols:
            if col == self.cols[0]:
                if reverse:
                    ms = ms.order_by(SecurityActivities.cost)
                else:
                    ms = ms.order_by(-SecurityActivities.cost)
            if col == self.cols[1]:
                if reverse:
                    ms = ms.order_by(SecurityActivities.maintenance)
                else:
                    ms = ms.order_by(-SecurityActivities.maintenance)
            if col == self.cols[2]:
                if reverse:
                    ms = ms.order_by(SecurityActivities.efficiency)
                else:
                    ms = ms.order_by(-SecurityActivities.efficiency)
        return ms.all()

