#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = 'penny'

from getdb import GetDB
from sendmail import SendMail

class SlaveStatu:
    error = []

    def __init__(self):
        self.master = GetDB('./config.ini', 'DATABASE3')
        self.master_conn = self.master.get_conn()
        self.master_cur = self.master_conn.cursor()
        self.slave = GetDB('./config.ini', 'DATABASE4')
        self.slave_conn = self.slave.get_conn()
        self.slave_cur = self.slave_conn.cursor()

    def isSlave(self):
        """
        数据库同步是否正常
        :return: None同步未开启,False同步中断,True同步正常
        """
        self.slave_cur.execute("SHOW SLAVE STATUS")
        result = self.slave_cur.fetchone()
        #判断Slave_SQL_Running Slave_IO_Running都为yes
        if result:
            if result[10] == "Yes" and result[11] == "Yes":
                self.slave_cur.close()
                return True
            else:
                if result[10] == "No":
                    self.error.append( result[35] )
                else:
                    self.error.append( result[37] )
                return False

    def synchron(self):
        '''
        开启同步
        :return:
        '''
        #获取master的File、Position
        self.master_cur.execute("SHOW MASTER STATUS")
        result = self.master_cur.fetchone()
        self.master_cur.close()
        #slave 重新同步
        self.slave_cur.execute("STOP SLAVE")
        self.slave_cur.execute("SHOW MASTER STATUS")
        host,port,user,passwd = self.master.dbinfo()
        #change master to master_host='10.122.74.230',master_port=3306,master_user='testadmin',master_password='test123infobird',master_log_file='binlog.000026' ,master_log_pos=512367644
        sql = "change master to master_host='{0}',master_port={1},master_user='{2}',master_password='{3}',master_log_file='{4}',master_log_pos={5};".format(host,port,user,passwd,result[0],result[1])
        self.slave_cur.execute(sql)
        self.slave_cur.execute("START SLAVE")
        self.slave_cur.close()

    def get_last_error(self):
        """
        获取第一个错误信息
        :return: String
        """
        if self.error:
            return self.error.pop(0)

    def close(self):
        '''关闭数据库连接'''
        self.master_conn.close()
        self.slave_conn.close()

def main():
    slave = SlaveStatu()
    isSlave = slave.isSlave()
    if isSlave:
        slave.close()
    else:
        slave.synchron()
        slave.close()
        error = slave.get_last_error()
        sendMail = SendMail('./config.ini', 'MAIL', '{0}'.format(error))
        sendMail.send_mail()

if __name__ == "__main__":
   main()