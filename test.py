# -*- coding:utf-8 -*-
import os
import random
import uiautomator2 as u2
import re
import json
from time import sleep
import time
from File import file
import time,threading
def test(dev,token):
    print dev
    time.sleep(100)

if __name__ == '__main__':
    devices = os.popen('adb devices').read().splitlines()
    device_list = []
    for i in range(1, devices.__len__()):
        if 'device' in devices[i]:
            if 'List' not in devices[i]:
                device_list.append(devices[i][:-7])
    if device_list == []:
            time.sleep(10000)
    device_list=['123','1234','12345']
    #token = json.loads(open('token.txt', 'r').read())['token']
    for device in device_list:
        threading.Thread(target=test,args=(device.strip('\n'),'1')).start()

#os.popen('python -m uiautomator2 init')#
#deviceid='53476787'
# d = u2.connect('127.0.0.1:62001')
# while True:
#     d(resourceId='com.sina.weibo:id/comment').click_exists(100)
#     d(resourceId='com.sina.weibo:id/edit_view').set_text(file().sh())
#     d(text='发送').click_exists(100)
#d.press(5)
#d.app_start('com.dobe.sandbox')
#d.app_stop('com.dobe.sandbox')
#d.service("uiautomator").stop()

# d(text='设置').click_exists(10)
# d(text='帐号与安全').click_exists(10)
# d(text='登录设备管理').click_exists(10)

# wxid = re.findall('(wxid_[0-9a-z]{1,100})', d(resourceId='com.tencent.mm:id/czz').get_text())[0]
# print wxid
#d(resourceId='tcaptcha_drag_thumb').drag_to(750,1000).drag_to(850,1000)

#d.app_stop('com.dobe.sandbox')
#d.app_start('com.dobe.sandbox')
#d(resourceId="com.dobe.sandbox:id/context_menu").long_click(3)



#d.swipe_points(list, 0.05)
#d.swipe_points([(0.235, 0.456), (0.503, 0.449), (0.509, 0.601), (0.777, 0.603), (0.771, 0.763), (0.222, 0.75)], 0.2)
# d(resourceId="com.dobe.sandbox:id/context_menu")[0].click()
# d(text="清除APP数据").click()
#
# d(text="确认删除").click()
# sleep(3)
# d(resourceId="com.dobe.sandbox:id/download_device").click()
# sleep(3)
# d.press(4)
# d(text="修改设备").click()
# d(text="修改机型").click()
# d(resourceId="com.dobe.sandbox:id/appIc1on").click()
#d(resourceId="com.dobe.sandbox:id/appIcon").click()
