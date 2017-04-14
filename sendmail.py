#__author__ = 'penny'
# -*- coding:utf-8 -*-

import os,time
import configparser
import smtplib
from email.mime.text import MIMEText



class SendMail:
    '''定义发送邮件'''

    def __init__(self, ini_file,mail,mail_body):
        config = configparser.ConfigParser()

        # 从配置文件中读取
        config.read(ini_file, encoding='utf-8')
        self.sendTo = config[mail]['to_address']
        self.sender_name =  config[mail]['sender_name']
        self.sender_pswd =  config[mail]['sender_pswd']
        self.host =  config[mail]['host']
        self.subject = config[mail]['subject']
        self.mail_body = mail_body

    def __messages(self):
        '''生成邮件内容'''
        self.msg = MIMEText(self.mail_body, _subtype='html', _charset='utf-8')
        # 定义标题,
        self.msg['Subject'] = self.subject
        # 定义发送时间
        self.msg['date'] = time.strftime('%a, %d %b %Y%H:%M:%S %z')


    def send_mail(self):
        '''
        sub:主题
        content:内容
        send_mail("aaa@126.com","sub","content")
        '''
        self.__messages()
        self.msg['mail_from'] = self.sender_name
        try:
            smtp = smtplib.SMTP()
            smtp.connect(self.host)
            smtp.login(self.sender_name,self.sender_pswd)
            smtp.sendmail( self.msg['mail_from'], self.sendTo, self.msg.as_string())
            smtp.quit()
        except Exception:
            print("邮件发送失败")
            raise

if __name__ == '__main__':
    sendMail = SendMail('./config.ini','MAIL','io 出错')
    sendMail.send_mail()






