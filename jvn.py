'''
Created on 2018/03/17

@author: Zizhu Zhang
'''
import MySQLdb 
class Jvn:
    cur     =''
    conn      =''
    
    id      =''
    url     =''
    title   =''
    cvs_three=''
    cvs_two=''
    published_date=''
    update_date=''
    create_date = ''
    
    def __init__(self,_url,_title,_cvs_three,_cvs_two,_published_date,_update_date,_create_date):
         
        _idlist =_url.replace('.html','').rsplit('/')
        self.id=_idlist[len(_idlist)-1]
        self.url=_url
        self.title=_title
        self.cvs_three=_cvs_three
        self.cvs_two=_cvs_two
        self.published_date=_published_date
        self.update_date=_update_date
        self.create_date=_create_date
        
        self.connectmysql()
        
        
    def isInDB(self):        
        _flag = False
        self.cur.execute("SELECT id FROM jvn_summary where id='{0}'".format(self.id))
        for row in self.cur.fetchall():
            if row[0] == self.id:
                _flag= True
                break
            else:
                continue
        return _flag                    
         
        self.closemysql();
            
    def updateDB(self):
        print('update')
        #nothing
        
    def InsertDB(self):
        try:
            self.cur.execute("insert into jvn_summary(id,url,title,cvs_three,cvs_two,published_date,update_date,create_date)values('{0}','{1}','{2}',{3},{4},'{5}','{6}','{7}')".format(self.id,self.url,self.title,self.cvs_three,self.cvs_two,self.published_date,self.update_date,self.create_date))
        except MySQLdb.Error as e:
            self.conn.rollback()
        self.conn.commit()
        self.closemysql()
        
    def connectmysql(self):             
        conn = MySQLdb.connect(host="localhost",    
                         user="root",         
                         passwd="",  
                         db="jvn")
        conn.set_character_set('utf8')
#         conn.execute('SET NAMES utf8;')
#         conn.execute('SET CHARACTER SET utf8;')
#         conn.execute('SET character_set_connection=utf8;')
        self.conn=conn
        self.cur = conn.cursor()
        
    def validate(self):
        
        if self.id is None:
            return  False
        elif self.url is None:
            return  False
        elif self.title is None:
            return  False
        elif self.title is None:
            return  False
        elif self.cvs_three is None:
            return  False
        elif self.cvs_two is None:
            return  False
        elif self.published_date is None:
            return  False
        elif self.update_date is None:
            return  False
        elif self.create_date is None:
            return  False
        else:
            return True
    
    def action(self):
        if self.validate():
            if not self.isInDB():
                self.InsertDB()
                print('success')
            else:
                print('fail')
        
                    
    def closemysql(self):
        self.conn.close()
        