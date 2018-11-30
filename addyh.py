
#-*- encoding:utf-8 -*-
from File import file
support_file_name = '养号列表.txt'
support_Data = file.read(support_file_name)
error_file_name = '登录异常账号.txt'
error_Data_List = file.read_all(error_file_name)
wechat_file_name = '微信账号数据.txt'
wechat_Data_List = file.read(wechat_file_name)
num = []
import re

for support in support_Data:
    if 'True' not in support.strip('\n'):
        if re.findall('(.*)\|', support)[0] not in error_Data_List:
            for wechat_Data in wechat_Data_List:
                 if re.findall('(.*)\|', support)[0] in wechat_Data:
                       num.append('%s ID:%s' % (wechat_Data.strip('\n'), re.findall('\|(.*)', support)[0]))


with open('养号列表执行文本.txt'.decode('utf-8'),'w') as f:
     for i in num:
         f.write('%s\n'%i)

print '生成"养号列表执行文本"'.decode('utf-8')
