import web
from datetime import datetime as dt
import datetime
import time
import settings
import os
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')

here = os.path.abspath(os.path.dirname(__file__))
templates = here + '/templates/'
def render(params={}, partial=False):
    global_vars = dict(settings.GLOBAL_PARAMS.items() + params.items())
    if partial:
        return web.template.render(templates, globals=global_vars)
    else:
        return web.template.render(templates, base='layout', globals=global_vars)

render = web.template.render('templates/')
db = web.database(dbn='mysql', db='absense', user=settings.MYSQL_USERNAME, pw=settings.MYSQL_PASSWORD)
urls = (
    '/', 'index',
    '/calendar', 'calendar',
    '/api/events', 'events'
)

class index:
    def GET(self):
       # day = getAvaliableDay()
        day = get()
        result = ''
        date = dt.now()
        return render.index(day,result, date)
    
    def POST(self):
        result = []
        day = get()
        i = web.input()
        date_s = time.strptime(i.ddd,"%Y-%m-%d")
        date_c = datetime.datetime(*date_s[:3])
        ret = db.query('select * from ab where date="%s" and user_id in (7,8,1000)' % i.ddd)
        
        for i in ret:
            if i.user_id==7:
                name='Jeans'
            if i.user_id==8:
                name='Jean wife'
            if i.user_id==1000:
                name='stella'
            result.append({'name':name,'work': i.work})

        
        return render.index(day,result,date=date_c)

class calendar:
    def GET(self):

        return render.calendar()

class events:
    def GET(self):
        ret = []
        
        return json.dumps({"success":1, "result": ret})
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

def get():
    now=dt.now().strftime("%Y-%m-%d")
    ret = db.query('''select date from ab where date in
            (select date from ab where date in 
            (select date from ab where user_id=7 and work=False) 
            and user_id=8 and work=True) 
            and user_id=1000 and work=False and date >"%s" limit 1''' % now)
    for i in ret:
        date=i.date
    return date

def getDays():
    keys = []
    ret = db.query('''select date from ab where date in 
            (select date from ab where date insert  
            (select date from ab where user_id=7 and work=False)
            and user_id=8 and work=True)
            and user_id=1000 and work=False and date limit 1000''')
    for i in ret:
        keys.append(i.date)


def getAvaliableDay():
    start = dt(2013,10,19)
    oneday = datetime.timedelta(days=1)

    shift1 = [0,0,1,1]
    shift2 = [1,1,0,0,0]
    user_id = 1000
    i = 0
    while start <= dt(2014,12,1):
        if i%7==0 or i%7==1:
            db.insert('ab', user_id=user_id, date=start, work=False)
        else:
            db.insert('ab', user_id=user_id, date=start, work=True)
        start = start + oneday
        i += 1
    day = start
    return day

