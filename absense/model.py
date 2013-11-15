#!/usr/bin/python2.7 
# -*- coding: utf-8 -*-
import web
import settings

db = web.database(dbn='mysql', db='ab2', user=settings.MYSQL_USERNAME, pw=settings.MYSQL_PASSWORD)

class Zheng:
    def new(self, date, work_type):
        if work_type == 1 or work_type == 3:
            night = True
        elif work_type == 2 or work_type ==4:
            night = False
        return db.insert('zheng', date=date, work_type=work_type, night=night)

    def update(self, date, **kwd):
        try:
            if 'work_type' in kwd  and kwd['work_type']:
                db.update('zheng', where='date=$date', work_type=kwd['work_type'], vars=locals())

            return True
        except Exception, e:
            print e
            return False

