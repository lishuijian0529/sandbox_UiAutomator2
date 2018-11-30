# -*- coding:utf-8 -*-
import os
import time
from File import file
import logger
import requests
import logging
import random
import datetime
import TokenYZ
from Token import token
from weiba_api import WB
import json
import base64
import re
import uiautomator2 as u2

class login_wechat():
    def __init__(self, deviceid, gj_mode, wxid=None, login_mode=None, cloudCode=None, ip=None, date=None,switchingmode=None):
        self.deviceid = deviceid
        self.om = file().readOperationMode()
        self.gj_mode = gj_mode
        self.w = WB(self.deviceid)
        self.wxid = wxid
        self.login_mode = login_mode
        self.cloudCode = cloudCode
        self.ip = ip
        self.date = date
        self.switchingmode=switchingmode
        self.element_json = json.loads(file.read_all('6.7.3.json'))
        self.d = u2.connect(self.deviceid)

    def sandbox_login(self, ph, mm):
        with open('跳辅设置.txt'.decode('utf-8'), 'r')as f:
            mode = json.loads(f.read())['transmission_mode']
        os.popen('adb -s %s shell rm -rf /sdcard/boxbackup' % self.deviceid)
        os.popen('adb -s %s shell mkdir /sdcard/boxbackup' % self.deviceid)
        fsize = int(round(os.path.getsize('package/%s/%s' % (self.deviceid, self.cloudCode)) / float(1024 * 1024), 2)) - 2
        with open('沙盒账密配置.json'.decode('utf-8'), 'r') as f:
            a = json.loads(f.read())
        for i in a:
            if self.deviceid == i['deviceid']:
                username = i['username']
                password = i['password']
        if mode == 'ftp':
            with open('server_config.txt', 'r') as f:
                data = json.loads(f.read())
            time.sleep(2)
            os.popen('start adb -s %s shell curl ftp://%s/package/%s/%s -o /sdcard/boxbackup/%s'%(self.deviceid,data['host'],self.deviceid,self.cloudCode,self.cloudCode))
        if mode == 'adb':
            self.d.push('Maintain/%s'%(self.cloudCode),'/sdcard/boxbackup/%s'%(self.cloudCode))
            #os.popen('start adb -s %s push package/%s/%s /sdcard/boxbackup/%s' %(self.deviceid,self.deviceid,self.cloudCode,self.cloudCode))
        time.sleep(2)
        #while True:
        #    time.sleep(3)
        #    try:
        #        sj_fsize = re.findall('([0-9]{1,3})M', os.popen('adb -s %s shell ls -lh sdcard/boxbackup/%s'%(self.deviceid,self.cloudCode)).read())[0]
        #        logging.info(u'%s-正在检查文件传输状态,请稍等' % self.deviceid)
        #        if int(sj_fsize) > int(fsize):
        #            logging.info(u'%s-文件传输完毕'% self.deviceid)
        #            break
        #    except:
        #        pass
        self.d.app_stop('com.dobe.sandbox')
        self.d.app_start('com.dobe.sandbox')
        if self.d(resourceId='com.dobe.sandbox:id/download_icon').exists(60)==True:
            self.d(resourceId='com.dobe.sandbox:id/download_icon').click()
        wz = self.d(resourceId='com.dobe.sandbox:id/textView').get_text()
        while True:
            if wz.encode('utf-8') == '尚未登陆,点击登陆':
                self.d(text='尚未登陆,点击登陆').click()
                self.d(resourceId='com.dobe.sandbox:id/editText').set_text(username)
                self.d(resourceId='com.dobe.sandbox:id/editText2').set_text(password)
                time.sleep(1)
                self.d.press(66)
                time.sleep(1)
                self.d(text='点击登陆').click()
                if self.d(resourceId='com.dobe.sandbox:id/download_icon').exists(60)==True:
                    break
            else:
                time.sleep(1)
                self.d.press(4)
                break
        self.d(resourceId='com.dobe.sandbox:id/context_menu').click()
        self.d(text='清除APP数据').click()
        self.d(text='确认删除').click()
        time.sleep(5)
        self.d(resourceId='com.dobe.sandbox:id/download_device').click()
        self.d(text='备份恢复').click()
        while True:
            if self.d(resourceId='com.dobe.sandbox:id/backup_info').exists(1)==True:
                self.d(resourceId='com.dobe.sandbox:id/backup_info').click()
                self.d(text='确定').click()
                break
        time.sleep(10)
        self.d.app_stop('com.dobe.sandbox')
        time.sleep(3)
        self.d.app_start('com.dobe.sandbox')
        if self.d(resourceId='com.dobe.sandbox:id/context_menu').exists(10)==True:
            self.d(resourceId='com.dobe.sandbox:id/appIcon').click()

        return ph,mm

    def visualization(self, message):
        try:
            requests.get('http://127.0.0.1:666/query?time=%s&number=%s&state=%s' % (int(time.time()), self.deviceid, message))
        except:pass

    def error_message(self):
        while True:
            if '外挂' in self.cw.encode('utf-8'):
                return 'waigua'
            if '批量' in self.cw.encode('utf-8'):
                return 'piliang'
            if '密码错误' in self.cw.encode('utf-8'):
                return 'piliang'
            if '多人投诉' in self.cw.encode('utf-8'):
                return 'tousu'
            if '系统检测' in self.cw.encode('utf-8'):
                return 'xitong'
            if '微信登陆环境存在异常' in self.cw.encode('utf-8'):
                return 'huanjingyichang'
            if '添加好友' in self.cw.encode('utf-8'):
                return 'tianjia'
            if '使用存在异常' in self.cw.encode('utf-8'):
                return 'shiyongyichang'
            if '传播色情' in self.cw.encode('utf-8'):
                return 'seqing'
            if '长期未登陆' in self.cw.encode('utf-8'):
                return 'changqi'
            if '你的微信号由于长期' in self.cw.encode('utf-8'):
                return 'weishiyong'
            if '解封环境异常' in self.cw.encode('utf-8'):
                return 'jiefengyichang'
            if '手机通讯录' in self.cw.encode('utf-8'):
                self.d(text='否').click()
                return None
            if '表情' in self.cw.encode('utf-8'):
                self.d(text='　取消　').click()
                return None
            if '通过短信验证码' in self.cw.encode('utf-8'):
                self.d(text='确定').click()
                return None
            if '注册了新的微信号' in self.cw.encode('utf-8'):
                return 'newwechat'



    def mm_login(self, ph, mm):
        time.sleep(20)
        while True:
            #如果出现输入框
            if self.d(resourceId=self.element_json[u'输入框ID']).exists(2)==True:
                if self.d(resourceId='com.tencent.mm:id/ji').exists(10)==True:
                    self.d(resourceId='com.tencent.mm:id/ji').set_text(mm)
                logging.info(self.deviceid + u'-输入密码')
                self.d(resourceId='com.tencent.mm:id/ch6').click()
                logging.info(self.deviceid + u'-点击登录')
                if self.d(resourceId='com.tencent.mm:id/cvo').exists(10)==True:
                    # 判断是否登录不上
                    self.cw = self.d(resourceId='com.tencent.mm:id/cvo').get_text()
                    if '表情' in self.cw.encode('utf-8'):
                        self.d(text='取消').click()
                        break
                    if '通过微信密码' in self.cw.encode('utf-8'):
                        self.d(text='忽略').click()
                        break
                    else:
                        return self.error_message()
            if self.d(resourceId='com.tencent.mm:id/cvo').exists(2)==True:
                logging.info(u'%s-发现错误弹窗'%self.deviceid)
                self.cw = self.d(resourceId='com.tencent.mm:id/cvo').get_text()
                if '表情' in self.cw.encode('utf-8'):
                    self.d(text='取消').click()
                if '通过微信密码' in self.cw.encode('utf-8'):
                    self.d(text='忽略').click()
                    break
                else:
                    self.d(resourceId='com.tencent.mm:id/au_').click()
                    logging.info(u'%s-点击确定' % self.deviceid)
                    logging.info(self.deviceid + u'-登陆出现错误')
                    logging.info(u'%s-打开微信' % self.deviceid)
            #如果进入微信页面
            if self.d(resourceId='com.tencent.mm:id/cw2').exists(2)==True:
                break
            #如果进入微信首页
            if self.d(resourceId='com.tencent.mm:id/dbe').exists(2) == True:
                self.Home_Login(ph, mm)
                while True:
                    if self.d(resourceId='com.tencent.mm:id/cvo').exists(2)== True:
                        self.cw = self.d(resourceId='com.tencent.mm:id/cvo').get_text()
                        return self.error_message()
                    if self.d(description='拖动下方滑块完成拼图').exists(2)==True:
                        return 'huatu'
                    if self.d(text='拖动下方滑块完成拼图').exists(2)==True:
                        return 'huatu'
            if self.d(resourceId='com.dobe.sandbox:id/appIcon').exists(2)==True:
                self.d(resourceId='com.dobe.sandbox:id/appIcon').click()

    def Home_Login(self,ph,mm):
        self.d(text='登录').click()
        self.d(resourceId=self.element_json[u'输入框ID']).click()
        os.system('adb -s %s shell input text %s' % (self.deviceid, ph))
        logging.info(self.deviceid + u'-输入账号')
        self.d(resourceId=self.element_json[u'输入手机号码登陆下一步']).click()
        logging.info(self.deviceid + u'-下一步')
        self.d(resourceId=self.element_json[u'输入框ID'])[1].click()
        os.system('adb -s %s shell input text %s' % (self.deviceid, mm))
        logging.info(self.deviceid + u'-输入密码')
        self.d(resourceId=self.element_json[u'输入手机号码登陆下一步']).click()
        logging.info(self.deviceid + u'-登录')




    def login_fail(self, error, wechat_list):
        if error == 'waigua':
            file().write('%s %s %s %s 外挂 %s\n' % (wechat_list[0], wechat_list[1], self.ip, self.date, self.deviceid),'登录异常账号.txt')
        if error == 'piliang':
            file().write('%s %s %s %s 批量 %s\n' %(wechat_list[0], wechat_list[1], self.ip, self.date, self.deviceid),'登录异常账号.txt')
        if error == 'mimacuowu':
            file().write('%s %s %s %s 密码错误 %s\n' % (wechat_list[0], wechat_list[1], self.ip, self.date, self.deviceid),'登录异常账号.txt')
        if error == 'tousu':
            file().write('%s %s %s %s 多人投诉被限制登陆 %s\n' % (wechat_list[0], wechat_list[1],self.ip,self.date, self.deviceid), '登录异常账号.txt')
        if error == 'jidiao':
            file().write('%s %s %s %s 在别的设备登陆过 %s\n' % (wechat_list[0], wechat_list[1],self.ip,self.date, self.deviceid),'登录异常账号.txt')
        if error == 'xitong':
            file().write('%s %s %s %s 系统检测到你的账号有异常 %s\n' % (wechat_list[0], wechat_list[1], self.ip,self.date,self.deviceid),'登录异常账号.txt')
        if error == 'huanjingyichang':
            file().write('%s %s %s %s 当前设备的微信登陆环境存在异常 %s\n' % (wechat_list[0], wechat_list[1],self.ip,self.date, self.deviceid),'登录异常账号.txt')
        if error == 'tianjia':
            file().write('%s %s %s %s 当前账号添加好友过于频繁 %s\n' % (wechat_list[0], wechat_list[1],self.ip,self.date ,self.deviceid),'登录异常账号.txt')
        if error == 'shiyongyichang':
            file().write('%s %s %s %s 当前账号的使用存在异常 %s\n' % (wechat_list[0], wechat_list[1], self.ip,self.date,self.deviceid),'登录异常账号.txt')
        if error == 'seqing':
            file().write('%s %s %s %s该微信账号因涉嫌传播色情 %s\n' % (wechat_list[0], wechat_list[1],self.ip,self.date, self.deviceid), '登录异常账号.txt')
        if error == 'changqi':
            file().write('%s %s %s %s 该账号长期未登陆 %s\n' % (wechat_list[0], wechat_list[1], self.ip,self.date,self.deviceid),'登录异常账号.txt')
        if error == 'huatu':
            file().write('%s %s %s %s 进入滑图页面 %s\n' % (wechat_list[0], wechat_list[1],self.ip,self.date, self.deviceid),'登录异常账号.txt')
        if error == 'weishiyong':
            file().write('%s %s %s %s 该账号长期未使用,已被收回 %s\n' % (wechat_list[0], wechat_list[1], self.ip, self.date, self.deviceid),'登录异常账号.txt')
        if error == 'jiefengyichang':
            file().write( '%s %s %s %s 解封环境异常 %s\n' % (wechat_list[0], wechat_list[1], self.ip, self.date, self.deviceid), '登录异常账号.txt')
        if error == 'newwechat':
            file().write('%s %s %s %s 注册了新的微信号 %s\n' % (wechat_list[0], wechat_list[1], self.ip, self.date, self.deviceid),'登录异常账号.txt')
        if error == 'huatu':
            file().write('%s %s %s %s 出现滑图 %s\n' % (wechat_list[0], wechat_list[1], self.ip, self.date, self.deviceid),'登录异常账号.txt')
    def add_friend(self, zh, mm, hy):
        if self.d(resourceId=self.element_json[u'微信页面加号']).exists(100)==True:
            self.d(resourceId=self.element_json[u'微信页面加号']).click()
        if self.d(resourceId=self.element_json[u'加号列表']).exists(100)==True:
            self.d(resourceId=self.element_json[u'加号列表'])[1].click()
        logging.info(self.deviceid + u'-添加朋友')
        if self.d(resourceId=self.element_json[u'输入框ID']).exists(100)==True:
            self.d(resourceId=self.element_json[u'输入框ID']).set_text(hy)
        time.sleep(3)
        if self.d(resourceId=self.element_json[u'点击添加按钮']).exists(100)==True:
            self.d(resourceId=self.element_json[u'点击添加按钮']).set_text(hy)
        while True:
            if self.d(resourceId=self.element_json[u'设置备注']).exists(2) == True:
                break
            if self.d(resourceId=self.element_json[u'错误弹窗确定ID']).exists(2) == True:
                self.d(resourceId=self.element_json[u'错误弹窗确定ID']).click()
                time.sleep(3)
                self.d(resourceId=self.element_json[u'点击添加按钮']).click()
        while True:
            if self.d(resourceId=self.element_json[u'添加通讯录']).exists(2) == True:
                self.d(resourceId=self.element_json[u'添加通讯录']).click()
            if self.d(resourceId=self.element_json[u'发消息']).exists(2) == True:
                self.d(resourceId=self.element_json[u'发消息']).click()
            if self.d(resourceId=self.element_json[u'消息内容框ID']).exists(2) == True:
                break
        self.d(resourceId=self.element_json[u'消息内容框ID']).set_text(zh)
        logging.info(self.deviceid + u'-正在发送信息:' + zh)
        self.visualization('正在发送信息:%s' % zh)
        time.sleep(5)
        self.d(resourceId=self.element_json[u'消息发送按钮ID']).click()
        logging.info(self.deviceid + u'-点击发送')
        time.sleep(2)
        if self.gj_mode == '1.微霸改机'.decode("utf-8"):
            file().writehy('%s_%s  %s  %s  %s  %s| %s' % (
            self.wechat_list[0], self.wechat_list[1], datetime.datetime.now().strftime('%Y-%m-%d'), self.deviceid, self.
                wxid, self.cloudCode, hy))
        else:
            file().writehy('%s  %s  %s %s' % (zh, mm, self.deviceid,hy))

    def circle_of_friends(self):
        self.d(resourceId=self.element_json[u'微信四个主按钮ID'])[2].click()
        logging.info(self.deviceid + u'-点击发现')
        self.d(resourceId=self.element_json[u'发现页面朋友圈ID'])[0].click()
        logging.info(self.deviceid + u'-点击朋友圈')
        time.sleep(2)
        self.d(resourceId=self.element_json[u'朋友圈相机ID']).long_click(3)
        logging.info(self.deviceid + u'-长按相机')
        if self.d(resourceId=self.element_json[u'发表按钮ID']).exists(5)==True:
            self.input_message()
        else:
            self.d(resourceId=self.element_json[u'我知道了ID']).click()
            self.input_message()
        self.visualization('点击发表')
        logging.info(self.deviceid + u'-点击发表')
        self.d(description='返回').click()
        time.sleep(random.randint(1, 3))
        self.d(resourceId=self.element_json[u'微信四个主按钮ID']).click()
        time.sleep(random.randint(1, 3))
        file().write_pyq_succ('%s  %s  %s  %s' % (self.wechat_list[0], self.wechat_list[1], datetime.datetime.now().strftime('%Y-%m-%d'), self.deviceid))

    def input_message(self):
        time.sleep(random.randint(1, 2))
        self.visualization('进入到发文字朋友圈页面')
        logging.info(self.deviceid + u'-进入到发文字朋友圈页面')
        self.d(resourceId=self.element_json[u'朋友圈内容输入框ID']).click()
        self.d(resourceId=self.element_json[u'朋友圈内容输入框ID']).set_text(file.sh())
        logging.info(self.deviceid + u'-输入文字')
        time.sleep(random.randint(1, 2))
        self.d(resourceId=self.element_json[u'发表按钮ID']).click()

    #打开影子科技
    def start_yz(self):
        os.system('adb -s ' + self.deviceid + ' shell am force-stop wechatscancoder.jionego.com.wechatscancoder')
        os.popen('adb -s %s shell am start -n wechatscancoder.jionego.com.wechatscancoder/.MainActivity' % self.deviceid).read()
        time.sleep(3)
        os.popen('adb -s %s shell am start -n com.tencent.mm/.ui.LauncherUI' % self.deviceid).read()

    #获取62二维码
    def get_qr_image(self):
        folder = os.path.exists('./%s' % self.deviceid)
        if not folder:
            os.makedirs('./%s' % self.deviceid)
        else:
            pass
        res = requests.get('http://193.112.218.104:89/api?str=Initialize').text
        image = json.loads(res)['qrcode']
        data_62 = json.loads(res)['data']
        h = open("./%s/%s.jpg" % (self.deviceid, self.deviceid), "wb")
        h.write(base64.b64decode(image))
        h.close()
        os.popen('adb -s %s push ./%s/%s.jpg  /sdcard/myData/%s.jpg' % (self.deviceid, self.deviceid,  self.deviceid,self.deviceid)).read()
        time.sleep(2)
        os.popen('adb -s %s shell mv /sdcard/myData/%s.jpg /sdcard/myData/scan.jpg' % (self.deviceid, self.deviceid)).read()
        time.sleep(2)
        os.popen('adb -s %s shell curl http://127.0.0.1:8089?api=scandCode' % self.deviceid)
        time.sleep(3)
        for i in range(0, 10):
            os.popen('adb -s %s shell input tap 524 1587' % self.deviceid)
        return data_62

    def check_62(self):
        try:
            data = open('config.ini', 'r').read()
            return json.loads(data)['62'], json.loads(data)['A16']
        except:
            with open('config.ini', 'w') as f:
                f.write('{"62":"False","A16":"False"}')
            return "False", "False"



    def smjhy(self, ph=None, mm=None, device_token=None, hy=None):
        try:
            self.wechat_list = self.sandbox_login(ph, mm)
            self.error = self.mm_login(self.wechat_list[0], self.wechat_list[1])
            if self.error != None:
                self.login_fail(self.error, self.wechat_list)
            else:
                self.add_friend(self.wechat_list[0], self.wechat_list[1], hy)
                self.visualization('成功')
                logging.info(self.deviceid + u'-成功')
        except:
            logging.info(self.deviceid + u'-失败')


    #发朋友圈
    def fpyq(self, ph=None, mm=None, device_token=None):
        try:
            self.wechat_list = self.sandbox_login(ph, mm)
            self.error = self.mm_login(self.wechat_list[0], self.wechat_list[1])
            if self.error != None:
                self.login_fail(self.error, self.wechat_list)
            else:
                self.circle_of_friends()
                self.visualization('成功')
                logging.info(self.deviceid + u'-成功')
        except:
            logging.info(self.deviceid + u'-失败')

    #登录

    def T_A16(self, ph, mm):
        A16_list = []
        file_list = os.popen('adb -s %s shell ls /data/data/com.tencent.mm/files/kvcomm/'% self.deviceid).readlines()
        try:
            for _file in file_list:
                    os.system('adb -s %s shell su root chmod a+rw /data/data/com.tencent.mm/files/kvcomm/%s' % (self.deviceid,_file))
                    file_data = os.popen('adb -s %s shell su root cat -v /data/data/com.tencent.mm/files/kvcomm/%s' % (self.deviceid,_file)).read()
                    A16 = re.findall(',(A[0-9a-z]{15})', file_data)
                    if A16 != []:
                        A16_list.append(A16[0])
            device_data = os.popen('adb -s %s shell curl "http://127.0.0.1:8888/cmd?group=AppTool\&action=getHookDevice' % self.deviceid).read()
            data = json.loads(device_data)['data']
            file().write('%s|%s|%s|%s|%s|%s|%s|%s\n' % (ph, mm, A16_list[0], data['phone']['Imei'], data['build']['ANDROIDID'], data['phone']['BSSID'], data['build']['CPU_ABI'], data['build']['BRAND']), 'A16数据.txt')
            self.visualization('提A16数据成功')
            logging.info(u'%s-提A16数据成功' % self.deviceid)
            token().huojian_t62(self.deviceid, TokenYZ.pdtoken())
        except:
            self.visualization('提A16数据失败')
            logging.info(u'%s-提A16数据失败' % self.deviceid)

