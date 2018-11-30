# -*- coding: utf-8 -*-
import os
import re
from File import file
import datetime
import uiautomator2 as u2
from PhoneNumber import PhoneNumber
import logging
import TokenYZ
import random
from Token import token
from weiba_api import WB
import time
import json
import zipfile
import traceback
import Pack
import shutil
class newenvironment():
    def __init__(self, uid, password, pid, deviceid, o_username, o_password, wxmm, phmode, wxmc, phonenumber, gj_mode, tm=None, cooperator=None, country=None,gj=None,qh=None,switchingmode=None,filtering_mode=None,t=None,ip=None):
        self.uid = uid
        self.cooperator = cooperator
        self.password = password
        self.pid = pid
        self.deviceid = deviceid
        self.o_username = o_username
        self.o_password = o_password
        self.wxmm = wxmm
        self.phmode = phmode
        self.ph = PhoneNumber(self.uid, self.password, self.pid, self.deviceid, phmode)
        self.wxmc = wxmc
        self.gj_mode = gj_mode
        self.phonenumber = phonenumber
        self.tm = tm
        self.country = country
        self.gj = gj
        self.qh = qh
        self.w = WB(deviceid)
        self.element_json = json.loads(file.read_all('6.7.3.json'))
        self.switchingmode =switchingmode
        self.filtering_mode = filtering_mode
        self.t = t
        self.ip = ip
        self.d = u2.connect(self.deviceid)
    #微霸新机


    #沙盒新机
    def sand_box(self):
        os.popen('adb -s %s shell rm -rf /sdcard/boxbackup' % self.deviceid)
        with open('沙盒账密配置.json'.decode('utf-8'), 'r') as f:
            a = json.loads(f.read())
        for i in a:
            if self.deviceid == i['deviceid']:
                username = i['username']
                password = i['password']
        self.d.app_stop('com.dobe.sandbox')
        self.d.app_start('com.dobe.sandbox')
        self.d(resourceId='com.dobe.sandbox:id/download_icon').click()
        wz = self.d(resourceId='com.dobe.sandbox:id/textView').get_text()
        while True:
            if wz.encode('utf-8') == '尚未登陆,点击登陆':
                self.d(text='尚未登陆,点击登陆').click()
                self.d(resourceId='com.dobe.sandbox:id/editText').set_text(username)
                self.d(resourceId='com.dobe.sandbox:id/editText2').set_text(password)
                self.d.press(66)
                self.d(text='点击登陆').click()
                time.sleep(5)
                if self.d(resourceId='com.dobe.sandbox:id/download_icon')!=[]:
                    break
            else:
                self.d.press(4)
                break
        self.d(resourceId='com.dobe.sandbox:id/context_menu').click()
        self.d(text='清除APP数据').click()
        self.d(text='确认删除').click()
        time.sleep(5)
        self.d(resourceId='com.dobe.sandbox:id/download_device').click()
        self.d(text='修改设备').click()
        self.d(text='修改机型').click()
        b = 0
        while True:
            if self.d(className='android.widget.TextView')!=[]:
                list = self.d(className='android.widget.TextView')
                if list.__len__() > 5:
                    self.IMEI = re.findall('IMEI: (.*)', list[2].get_text())[0]
                    logging.info('%s-IMEI:%s' % (self.deviceid,self.IMEI))
                    self.MAC = re.findall('MAC: (.*)', list[5].get_text())[0]
                    logging.info('%s-MAC:%s' % (self.deviceid, self.MAC))
                    self.Brand = re.findall('BRAND: (.*)', list[6].get_text())[0]
                    logging.info('%s-BRAND:%s' % (self.deviceid, self.Brand))
                    self.d.press(4)
                    time.sleep(1)
                    self.d.press(4)
                    time.sleep(2)
                    self.d(resourceId='com.dobe.sandbox:id/appIcon').click()
                    break
                else:
                    if 5 == b:
                        raise Exception ,''
                    else:
                        b = b+1
                        time.sleep(2)
    #国内注册
    def register(self):
        self.d(resourceId=self.element_json[u'首页注册ID']).click()
        time.sleep(1)
        logging.info(self.deviceid + u'-点击注册')
    #国外输入账号信息

    def Judgment_Devices(self):
        while True:
            if os.system('adb -s %s shell cd /sdcard' % self.deviceid) != 0:
                logging.info(u'%s未检测到手机连接'%self.deviceid)
                time.sleep(5)
            else:
                break

    #国内输入账号信息
    def input_text(self):
        self.Judgment_Devices()
        self.d(resourceId=self.element_json[u'输入框ID'])[0].click_exists(100)
        #for i in  list(self.wxmc):
        #    time.sleep(0.3)
        #    os.system('adb -s %s shell input text %s'%(self.deviceid,i))
        self.d(resourceId=self.element_json[u'输入框ID'])[0].set_text(self.wxmc)
        logging.info(self.deviceid + u'-输入昵称')
        self.d(resourceId=self.element_json[u'输入框ID'])[1].set_text(self.phonenumber[0])
        self.Judgment_Devices()
        logging.info(self.deviceid + u'-清空手机号码')
        self.d(resourceId=self.element_json[u'输入框ID'])[1].click()
       #for i in  list(self.phonenumber[0]):
       #    time.sleep(0.3)
       #    os.system('adb -s %s shell input text %s'%(self.deviceid,i))
        logging.info(self.deviceid + u'-输入手机号码:' + self.phonenumber[0])
        #time.sleep(random.randint(1, 3))
        self.Judgment_Devices()
        self.d(resourceId=self.element_json[u'输入框ID'])[2].click()
        self.d(resourceId=self.element_json[u'输入框ID'])[2].set_text(self.wxmm)
        #for i in  list(self.wxmm):
        #    time.sleep(0.3)
        #    os.system('adb -s %s shell input text %s'%(self.deviceid,i))
        logging.info(self.deviceid + u'-输入密码:' + self.wxmm)
        #time.sleep(random.randint(1, 2))
        self.Judgment_Devices()
        self.d(resourceId=self.element_json[u'手机号注册页面注册按钮ID']).click()
        logging.info(self.deviceid + u'-点击注册')
        while True:
            if self.d(className=self.element_json['CheckBox']).exists(1) == True:
                self.d(className=self.element_json['CheckBox'])[0].click()
                time.sleep(1)
                logging.info(self.deviceid + u'-同意协议')
                os.popen('adb -s %s shell input tap 567 1789'%self.deviceid)
                time.sleep(5)
                break
            if self.d(resourceId=self.element_json[u'手机号注册页面注册按钮ID']).exists(1) == True:
                self.d(resourceId=self.element_json[u'手机号注册页面注册按钮ID']).click()
            if self.d(text='网页无法打开').exists(1) == True:
                self.d(text='网页无法打开').click()
                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                raise  Exception ,''
            if self.d(description="网页无法打开").exists(1) == True:
                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                raise Exception, ''
            if self.d(text='找不到网页').exists(1) == True:
                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                raise Exception, ''
        time.sleep(4)
        while True:
            if self.d(className=self.element_json['CheckBox']).exists(1) == True:
                self.d(className=self.element_json['CheckBox'])[0].click()
                logging.info(self.deviceid + u'-同意协议')
                os.popen('adb -s %s shell input tap 567 1789' % self.deviceid)
            if self.d(resourceId='com.tencent.mm:id/au_').exists(2) == True:
                self.d(resourceId='com.tencent.mm:id/au_').click()
            if self.d(text='微信安全').exists(1) == True:
                logging.info(self.deviceid + u'-进入滑图页面')
                break
            if self.d(text='网页无法打开').exists(1) == True:
                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                raise Exception , ''
            if self.d(description='网页无法打开').exists(1) == True:
                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                raise Exception, ''
            if self.d(text = '找不到网页').exists(1)==True:
                logging.info(self.deviceid + u'-找不到网页,网络不稳定,重新注册')
                raise Exception, ''
            os.popen('adb -s %s shell input tap 500 900' % self.deviceid)
            os.popen('adb -s %s shell input tap 460 1096' % self.deviceid)
            os.popen('adb -s %s shell input tap 507 1042' % self.deviceid)
        time.sleep(5)


    #滑图错误
    def error_Three_Months(self):
        if self.d(description='返回 ').exists(2) == True:
            logging.info(self.deviceid + u'-出现三个月,重新返回')
            if self.phmode == '14.玉米平台'.decode("utf-8"):
                self.ph.yumi_cancelSMSRecv(self.phonenumber[0], self.phonenumber[1])
            return '1'
        if self.d(description='操作超时，请重新发起(错误码: -22)').exists(2) == True:
            logging.info(self.deviceid + u'-操作超时')
            if self.phmode == '14.玉米平台'.decode("utf-8"):
                self.ph.yumi_cancelSMSRecv(self.phonenumber[0], self.phonenumber[1])
            return '1'


    #成功跳码
    def successful_Skip_Code(self):
        if self.d(resourceId=self.element_json['czl']).exists(2) == True:
            logging.info(self.deviceid + u'-跳码成功')
            return True

    #跳码失败直接退出
    def skip_Code_fail(self, error_type=None):
        if self.d(description='让用户用微信扫描下面的二维码').exists(2) == True:
            if error_type == 'Continue':
                logging.info(self.deviceid + u'-跳转到二维码页面')
            return False
        if self.d(text='让用户用微信扫描下面的二维码').exists(2) == True:
            if error_type == 'Continue':
                logging.info(self.deviceid + u'-跳转到二维码页面')
            return False
    # 国内图片验证
    def yztp(self):
        """
        验证图片 
        """
        if self.tm == '9':
            while True:
                if self.d(text='安全校验').exists(2) == True:
                    if self.skip_Code_fail('Continue') == False:
                        return False
                    if self.error_Three_Months() == False:
                        return False
                self.Judgment_Devices()
                if self.d(resourceId=self.element_json[u'短信内容ID']).exists(2) == True:
                    return True
                if self.d(text='开始 ').exists(1) == True:
                    os.popen('adb -s %s shell input swipe 50 1000 1000 1000 3000' % self.deviceid)
                if self.d(description='开始 ').exists(1) == True:
                    os.popen('adb -s %s shell input swipe 50 1000 1000 1000 3000' % self.deviceid)
                if self.d(text='开始').exists(1) == True:
                    os.popen('adb -s %s shell input swipe 50 1000 1000 1000 3000' % self.deviceid)
                if self.d(description='开始').exists(1) == True:
                    os.popen('adb -s %s shell input swipe 50 1000 1000 1000 3000' % self.deviceid)

        if self.tm == '6':
            while True:
                try:
                    for j in range(851, 951, 30):
                        self.d.touch.down(250, 1000)
                        for i in range(300, 760, 50):
                            time.sleep(0.01)
                            self.d.touch.move(i, random.randint(200, 1000))
                        for i in range(750, j, 10):
                            time.sleep(0.1)
                            self.d.touch.move(i, random.randint(200, 1000))
                        self.d.touch.up(j, 1000)
                        self.Judgment_Devices()
                        if self.d(text='安全校验').exists(2)==True:
                            if self.skip_Code_fail('Continue') == False:
                                return False
                            if self.error_Three_Months() == False:
                                return False
                        self.Judgment_Devices()
                        if self.d(resourceId=self.element_json[u'短信内容ID']).exists(2) == True:
                            return True
                        if self.d(text='开始 ').exists(1) == True:
                            os.popen('adb -s %s shell input swipe 50 1000 1000 1000 3000' % self.deviceid)
                        if self.d(description='开始 ').exists(1) == True:
                            os.popen('adb -s %s shell input swipe 50 1000 1000 1000 3000' % self.deviceid)
                        if self.d(text='开始').exists(1) == True:
                            os.popen('adb -s %s shell input swipe 50 1000 1000 1000 3000' % self.deviceid)
                        if self.d(description='开始').exists(1) == True:
                            os.popen('adb -s %s shell input swipe 50 1000 1000 1000 3000' % self.deviceid)
                except:pass
    #国内判断跳码
    def qr_validation(self, status):
        """
        判断是否跳码成功
        """
        if status == '1':
            raise  Exception,''
        if status == False:
            if self.tm == '9' or self.tm == '6':
                logging.info(self.deviceid + u'-未跳码成功,重新注册!')
                if self.phmode == '3.火箭API'.decode("utf-8"):
                    self.ph.hj_fail(TokenYZ.pdtoken(), self.phonenumber[1])
                if self.phmode == '9.老九专属API'.decode("utf-8"):
                    file().wite_lj_NotHopCode(self.phonenumber[0])
                if self.phmode == '2.菜鸟平台'.decode('utf-8'):
                    self.ph.cn_lh(self.phonenumber[0], self.phonenumber[1])
                if self.phmode == '12.国内私人3'.decode('utf-8'):
                    self.ph.grsr3_lh(self.phonenumber[1])
                if self.phmode == '13.国内私人4'.decode('utf-8'):
                    self.ph.grsr4_lh(self.phonenumber[1])
                raise Exception,''
        if status == True:
            dx = re.findall('[a-z0-9]{1,10}',self.d(resourceId=self.element_json[u'短信内容ID']).get_text())[0]
            logging.info(self.deviceid + u'-读取的短信内容为:' + dx)
            if self.phmode == '14.玉米平台'.decode("utf-8"):
                return self.yumi_sendmsg(dx)
            if self.phmode == '2.菜鸟平台'.decode('utf-8'):
                return self.ph.cn_send(self.phonenumber[1], dx)
            if self.phmode == '3.火箭API'.decode("utf-8"):
                #如果火箭平台返回True代表发送成功
                hj_status = self.ph.send_text(TokenYZ.pdtoken(), self.phonenumber[1], dx)
                if hj_status == True:
                    # 如果火箭平台返回True则返回一个succ
                    return 'succ'
            if self.phmode == '7.辽宁API'.decode("utf-8"):
                ln_status=self.ph.ln_send(self.phonenumber[0], dx)
                if ln_status == True:
                    return 'succ'
            if self.phmode == '8.国内私人1'.decode("utf-8"):
                return self.ph.gnsr_send_text(self.phonenumber[0], dx)
            if self.phmode == '9.老九专属API'.decode("utf-8"):
                return self.ph.lj_send_text(self.phonenumber[0], dx)
            if self.phmode == '10.国内私人2'.decode('utf-8'):
                return self.ph.gnsr2_send(self.phonenumber[0], dx)
            if self.phmode == '12.国内私人3'.decode('utf-8'):
                return self.ph.grsr3_send(self.phonenumber[1], dx)
            if self.phmode == '13.国内私人4'.decode('utf-8'):
                return self.ph.grsr4_send(self.phonenumber[1], dx)
            if self.phmode == '1.小鱼平台'.decode('utf-8'):
                return self.ph.xiaoyu_send_message(self.phonenumber[0], dx)
    #提交任务

    #玉米发短信
    def yumi_sendmsg(self, dx):
        try:
            yz = self.ph.yumi_sendmessages(dx, self.phonenumber[0], self.phonenumber[1])
            return yz
        except:
            logging.info(self.deviceid + u'-短信发送失败,卡商已下卡')

    #国外登录


    def T_A16(self,A16):
            file().write('%s|%s|%s|%s|%s|%s|%s|%s|\n' % (self.phonenumber[0], self.wxmm,A16, self.IMEI,self.ANDROID_ID ,self.MAC, self.CPU_ABI,self.Brand), 'A16数据.txt')
            logging.info(u'%s-提62成功' % self.deviceid)

    def scanCode(self,A16):
        if token().huojian_t62(self.deviceid, TokenYZ.pdtoken()) == True:
            self.T_A16(A16)

    #写入文件
    def xr_wechat(self,wxid=None,cloudCode=None,mf=None):
        logging.info(self.deviceid+u'-准备写入微信数据')
        wechat_list = '%s_%s  %s  %s  %s  %s  %s|\n' % (self.phonenumber[0], self.wxmm, self.ip, self.deviceid, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), wxid,cloudCode )
        file().write(wechat_list, '微信账号数据.txt')

    def send_login(self):
            if self.phmode == '8.国内私人1'.decode("utf-8"):
                self.ph.qg_card_add(TokenYZ.pdtoken(), self.phonenumber[0])
            time.sleep(8)
            logging.info(self.deviceid + u'-短信发送成功')
            if self.d(text='已发送短信，下一步').exists(100)==True:
                self.d(text='已发送短信，下一步').click()
            # 判断是否发送短信失败,点击下一步
            while True:
                self.Judgment_Devices()
                if self.d(text='不是我的，继续注册').exists(2)==True:
                    self.d(text='不是我的，继续注册').click()
                self.Judgment_Devices()
                if self.d(resourceId=self.element_json[u'错误弹窗确定ID']).exists(2)== True:
                    self.cw = self.d(resourceId=self.element_json[u'错误弹窗内容ID']).get_text()
                    if '短信' in self.cw.encode('utf-8'):
                        self.d(resourceId=self.element_json[u'错误弹窗确定ID']).click()
                        time.sleep(25)
                        self.d(text='已发送短信，下一步').click()
                        time.sleep(20)
                        if self.d(resourceId=self.element_json[u'错误弹窗确定ID']).exists(5) == True:
                            self.cw = self.d(resourceId=self.element_json[u'错误弹窗内容ID']).get_text()
                            if '短信' in self.cw.encode('utf-8'):
                                logging.info(self.deviceid + u'-已点击过"已发送短信，下一步"两次,还是未注册成功,进入重新注册流程')
                                raise Exception,''
                            if '逻辑' in self.cw.encode('utf-8'):
                                self.d(resourceId=self.element_json[u'错误弹窗确定ID']).click()
                                logging.info(self.deviceid + u'-已进入到微信页面,等待5秒判断是否出现秒封状况')
                                if self.d(resourceId=self.element_json[u'错误弹窗确定ID']).exists(5)==True:
                                    logging.info(self.deviceid + u'-账号秒封,重新注册')
                                    raise Exception,''
                                else:
                                    self.d(text='我').click()
                                    wxid = re.findall('(wxid_[0-9a-z]{1,100})',self.d(resourceId='com.tencent.mm:id/cl8').get_text())[0]
                                    logging.info('%s-微信ID:%s' % (self.deviceid, wxid))
                                    self.d(text='微信').click()
                                    time.sleep(1)
                                    self.d.press(4)
                                    while True:
                                        if self.d(resourceId='com.dobe.sandbox:id/appIcon').exists(2) == True:
                                            self.d(resourceId='com.dobe.sandbox:id/appIcon').click()
                                        if self.d(text='微信').exists(2) == True:
                                            break
                                        self.q(wxid)
                                        self.sandbox_save(wxid)
                                        break
                    if '异常' in self.cw.encode('utf-8'):
                        logging.info(self.deviceid + u'-该账号被秒封')
                        if self.gj_mode == '1.微霸改机'.decode("utf-8"):
                            self.save_wechat_data()
                            if self.w.save_wechat_data(self.phonenumber[0], self.wxid, self.wxmc) == True:
                                break
                    if '逻辑' in self.cw.encode('utf-8'):
                        self.d(resourceId=self.element_json[u'错误弹窗确定ID']).click()
                        logging.info(self.deviceid + u'-已进入到微信页面,等待5秒判断是否出现秒封状况')
                        if self.d(resourceId=self.element_json[u'错误弹窗确定ID']).exists(5)==True:
                            logging.info(self.deviceid + u'-账号秒封,重新注册')
                        else:
                            self.d(text='我').click()
                            wxid = \
                            re.findall('(wxid_[0-9a-z]{1,100})', self.d(resourceId='com.tencent.mm:id/cl8').get_text())[
                                0]
                            logging.info('%s-微信ID:%s' % (self.deviceid, wxid))
                            self.d(text='微信').click()
                            time.sleep(1)
                            self.d.press(4)
                            while True:
                                if self.d(resourceId='com.dobe.sandbox:id/appIcon').exists(2) == True:
                                    self.d(resourceId='com.dobe.sandbox:id/appIcon').click()
                                if self.d(text='微信').exists(2) == True:
                                    break
                                self.q(wxid)
                                self.sandbox_save(wxid)
                                break
                    if '一个月' in self.cw.encode('utf-8'):
                        logging.info(self.deviceid + u'-该手机号码一个月之内不能重复注册')
                        raise Exception,''
                    if '当天' in self.cw.encode('utf-8'):
                        logging.info(self.deviceid + u'-该手机号码当天不能重复注册')
                        os.popen('adb -s %s shell input keyevent 4' % self.deviceid).read()
                        time.sleep(3)
                        os.popen('adb -s %s shell input keyevent 4' % self.deviceid).read()
                        if self.d(resourceId=self.element_json[u'输入框ID']).exists(4)==True:
                            os.popen('adb -s %s shell input keyevent 4' % self.deviceid).read()
                            if self.d(resourceId=self.element_json[u'微信四个主按钮ID']).exists(10)==True:
                                pass
                    if '不正确' in self.cw.encode('utf-8'):
                        logging.info(self.deviceid + u'-发送的验证码不正确')
                        raise Exception,''
                    if '近期' in self.cw.encode('utf-8'):
                        logging.info(self.deviceid + u'-近期相同号码不可重复注册')
                        raise Exception,''
                self.Judgment_Devices()
                if self.d(text='微信').exists(2)==True:
                    logging.info(u'%s-已进入到微信页面,等待5秒判断是否出现秒封状况'%self.deviceid)
                    if self.d(resourceId=self.element_json[u'错误弹窗确定ID']).exists(5) == True:
                        logging.info(self.deviceid + u'-账号秒封,重新注册')
                    else:
                        self.d(text='我').click()
                        time.sleep(2)
                        try:
                            wxid = re.findall('(wxid_[0-9a-z]{1,100})', self.d(resourceId='com.tencent.mm:id/czz').get_text())[0]
                        except:
                            wxid = None
                        logging.info(u'%s-微信ID:%s' % (self.deviceid, wxid))
                        time.sleep(1)
                        self.q(wxid)
                        self.sandbox_save(wxid)
                        break
                #self.d.app_stop('com.dobe.sandbox')
                #self.d.app_start('com.dobe.sandbox')
                #self.Judgment_Devices()
                #time.sleep(2)
                # if self.d(resourceId='com.dobe.sandbox:id/context_menu').exists(30)==True:
                #     self.d(resourceId='com.dobe.sandbox:id/context_menu').click()
                #     self.Judgment_Devices()
                #     self.d(text='关闭进程').click()
                #     self.d(text='确认关闭').click()
                #     time.sleep(3)
                #     if self.d(resourceId='com.dobe.sandbox:id/appIcon').exists(20)==True:
                #         self.d(resourceId='com.dobe.sandbox:id/appIcon').click()
                #         time.sleep(5)

    def q(self,wxid):
        while True:
            if self.d(resourceId=self.element_json[u'错误弹窗确定ID']).exists(2)==True:
               raise Exception,''
            if self.d(resourceId=self.element_json[u'首页注册ID']).exists(2)==True:
                logging.info(self.deviceid + u'-账号被秒封')
                raise Exception, ''
            if self.d(resourceId=self.element_json[u'微信四个主按钮ID']).exists(2)==True:
                self.d(resourceId=self.element_json[u'微信四个主按钮ID'])[2].click()
                logging.info(self.deviceid + u'-点击发现')
                break
            if self.d(resourceId=self.element_json[u'输入框ID']).exists(2)==True:
                logging.info(self.deviceid + u'-账号被秒封')
                raise Exception, ''
        time.sleep(random.randint(1, 3))
        wechat_list = '%s_%s  %s  %s  %s  %s  \n' % (self.phonenumber[0], self.wxmm, self.ip, self.deviceid, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), wxid )
        file().write(wechat_list, '微信账号数据(不带环境包).txt')
        if self.d(text='朋友圈').exists(10)==True:
            self.d(text='朋友圈').click()
        else:
            logging.info(self.deviceid + u'-点击发现失败,重新点击')
            self.d(resourceId=self.element_json[u'微信四个主按钮ID'])[2].click()
            self.d(text='朋友圈').click()
        self.d(resourceId=self.element_json[u'朋友圈相机ID']).long_click(3)
        # 检测有没有朋友圈
        self.d(resourceId=self.element_json[u'我知道了ID']).click()
        self.input_pyq_message()
        logging.info(self.deviceid + u'-点击发表')
        time.sleep(3)

    def sandbox_save(self,wxid):
        self.d.press(3)
        time.sleep(3)
        os.popen('adb -s %s shell am start -n com.dobe.sandbox/.home.Main2Activity' % self.deviceid)
        self.d(resourceId='com.dobe.sandbox:id/appIcon').click_exists(100)
        self.d(resourceId=self.element_json[u'朋友圈相机ID']).exists(310)
        self.d.press(3)
        time.sleep(3)
        os.popen('adb -s %s shell am start -n com.dobe.sandbox/.home.Main2Activity' % self.deviceid)
        self.d(resourceId='com.dobe.sandbox:id/context_menu').click_exists(100)
        self.d(text='关闭进程').click_exists(100)
        self.d.service("uiautomator").stop()
        time.sleep(10)
        os.popen('adb -s %s shell input tap 500 1228'%self.deviceid)
        self.d(resourceId='com.dobe.sandbox:id/download_device').click_exists(100)
        self.d(text='备份恢复').click()
        self.d(text='+ 创建备份').click()
        os.popen('adb -s %s shell input text %s' % (self.deviceid, self.phonenumber[0]))
        self.d(text='确定').click()
        time.sleep(5)
        while True:
            time.sleep(2)
            if len(self.d(className='android.widget.ImageView'))<2:
                logging.info(u'%s-数据备份完成' % self.deviceid)
                if 'TextView' != self.d(resourceId='com.dobe.sandbox:id/backup_info').get_text():
                    break
                else:
                    os.popen('adb -s %s shell rm -rf /sdcard/boxbackup'%self.deviceid)
                    time.sleep(1)
                    self.d.press(4)
                    self.d(text='备份恢复').click()
                    self.Judgment_Devices()
                    self.d(text='+ 创建备份').click()
                    os.popen('adb -s %s shell input text %s' % (self.deviceid, self.phonenumber[0]))
                    self.Judgment_Devices()
                    self.d(text='确定').click()
        time.sleep(3)
        self.new_package = re.findall('(.*?).zip',os.popen('adb -s %s shell ls /sdcard/boxbackup'% self.deviceid).read().strip('\n'))[0]
        self.xr_wechat(wxid=wxid, cloudCode = self.new_package + '.zip')
        logging.info(self.deviceid + u'-注册数据已写入文件')
        self.new_package = re.findall('(.*?).zip', os.popen('adb -s %s shell ls /sdcard/boxbackup' % self.deviceid).read().strip('\n'))[0]
        self.d.pull('/sdcard/boxbackup/%s.zip'%self.new_package,'package/%s/%s.zip'%(self.deviceid,self.new_package))

        #os.popen(
        #    'start adb -s %s pull /sdcard/boxbackup/%s.zip package/%s/%s.zip' % (self.deviceid, self.new_package,self.deviceid,self.new_package))
        while True:
            try:
                f = zipfile.ZipFile("package/%s/%s.zip" % (self.deviceid, self.new_package), 'r')
                for file in f.namelist():
                    f.extract(file, "package/%s/0" % self.deviceid)
                break
            except:pass
        time.sleep(2)
        file_data = open('package/%s/0/0/hook/data.json' % self.deviceid, 'r').read()
        self.CPU_ABI = json.loads(file_data)['CPU_ABI']
        logging.info('%s-CPU_ABI:%s' % (self.deviceid, self.CPU_ABI))
        self.ANDROID_ID = json.loads(file_data)['android_id']
        logging.info('%s-ANDROID_ID:%s' % (self.deviceid, self.ANDROID_ID))
        A16_list = []
        for filename in os.listdir('package/%s/0/0/com.tencent.mm/files/kvcomm/' % self.deviceid):
            try:
                with open('package/%s/0/0/com.tencent.mm/files/kvcomm/%s' % (self.deviceid, filename), 'r') as f:
                    A16 = re.findall(
                        '(A[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z])',
                        f.read())
                    if A16 != []:
                        A16_list.append(A16[0])
            except:
                 pass
        Notes = zipfile.ZipFile(r'package/%s/%s.zip'%(self.deviceid,self.new_package), 'r').comment
        list = ['app_tbs', 'lib','tinker']
        logging.info(u'%s-A16:%s' % (self.deviceid, A16_list[0]))
        self.scanCode(A16_list[0])
        for i in list:
            try:
                Pack.remove_dir('package/%s/0/0/com.tencent.mm/%s' % (self.deviceid,i))
            except:pass
        for i in range(100,1000):
            try:
                Pack.remove_dir('package/%s/0/0/com.tencent.mm/app_xwalk_%s' % (self.deviceid, i))
            except:pass
        shutil.make_archive('package/%s/%s' % (self.deviceid,self.new_package), 'zip', r'package/%s/0'%(self.deviceid))
        zf = zipfile.ZipFile('package/%s/%s.zip' % (self.deviceid,self.new_package), 'a')
        zf.comment = Notes
        zf.close()
        time.sleep(2)
        try:
            Pack.remove_dir('package/%s/0'%self.deviceid)
        except:pass
        os.popen('adb -s %s rm -rf /sdcard/boxbackup' % self.deviceid)

    def save_wechat_data(self):
        self.wxid = self.w.get_wxid()
        self.cloudCode = self.w.getCloudCode(self.phonenumber[0])
        self.xr_wechat(self.wxid, self.cloudCode, 'True')
        logging.info(self.deviceid + u'-注册数据已写入文件')
        logging.info(self.deviceid + u'-正在保存微霸数据请稍等')
    # 国内登录
    def login_validation(self, yz):
        if yz == None:
            raise Exception , ''
        if yz == 'succ':
            self.send_login()

    #国内发圈
    def fpyq(self, yz):
        if yz == None:
            raise Exception, ''
        if yz == 'succ':
            self.send_login()
        else:
            logging.info(self.deviceid + u'-未接收到卡商反馈，注册失败')

    def input_pyq_message(self):
        time.sleep(random.randint(1, 2))
        self.d(resourceId=self.element_json[u'朋友圈内容输入框ID']).click()
        try:
            self.d(resourceId=self.element_json[u'朋友圈内容输入框ID']).set_text(file().sh())
        except:
            self.d(resourceId=self.element_json[u'朋友圈内容输入框ID']).set_text('My name is daduizhang')
        logging.info(self.deviceid + u'-输入文字')
        time.sleep(random.randint(1, 2))
        self.d(resourceId=self.element_json[u'发表按钮ID']).click()
    def pd_gj(self):

        self.sand_box()

    def new_zh(self):
        try:
            self.pd_gj()
            self.register()
            self.input_text()
            self.login_validation(self.qr_validation(self.yztp()))
        except:
            traceback.print_exc()
            logging.info(self.deviceid + u'-账号注册失败')

    def new_zhpyq(self):
        try:
            self.pd_gj()
            self.register()
            self.input_text()
            self.fpyq(self.qr_validation(self.yztp()))
        except:
            #traceback.print_exc()
            logging.info(self.deviceid + u'-账号注册失败')

    def gw_zc_t62_1280(self):
        pass

    def zc_pyq_t62(self):
        try:
            self.pd_gj()
            if self.country == '1.国内'.decode("utf-8"):
                self.register()
                self.input_text()
                self.fpyq(self.qr_validation(self.yztp()))
        except:
            traceback.print_exc()
            logging.info(self.deviceid + u'-账号注册失败')
            try:
                if self.phmode == '3.火箭API'.decode("utf-8"):
                    self.ph.hj_fail(TokenYZ.pdtoken(), self.phonenumber[1])
            except:pass
