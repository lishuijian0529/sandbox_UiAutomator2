# -*- coding: utf-8 -*-
import time
import logger
import logging
import os
from File import file
import re
import uiautomator2 as u2
from IP_Filtering import ip_fiter
class wj():
    def __init__(self,deviceid):
        self.deviceid = deviceid
        self.d = u2.connect(self.deviceid)
    def start(self,m,t,filtering_mode):
        self.appPackage = re.findall('(.*?)\|', file.read('平台账号.txt')[25].strip('\n'))[0]
        self.appActivity = re.findall('\|(.*)', file.read('平台账号.txt')[25].strip('\n'))[0]
        self.d.app_stop('com.tencent.mm')
        while True:
            self.d(resourceId='org.wuji:id/exit_vpn').click()
            time.sleep(int(t))
            try:
                ip = re.findall('[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}',self.d(resourceId='org.wuji:id/ips').get_text())[0]
                logging.info(self.deviceid + u"-VPN已成功连接")
                logging.info(self.deviceid + u"-IP:%s" % ip)
                if m == '1':
                    if ip_fiter(self.deviceid, ip, filtering_mode) == True:
                        return ip
                    else:
                        pass
                if m == '2':
                    if ip_fiter(self.deviceid, ip, filtering_mode) == True:
                        return ip
                    else:
                        pass
            except:
                time.sleep(10)
