# -*- coding:utf-8 -*-
import pika
import json
import os
import string
import re
import shutil
import zipfile
import tarfile
import zipfile, os

deviceid='127.0.0.1:62001'
#new_package='17cECC5FE6'
new_package = re.findall('(.*?).zip',os.popen('adb -s %s shell ls /sdcard/boxbackup'% deviceid).read().strip('\n'))[0]
print new_package
#os.popen('start adb -s %s pull /sdcard/boxbackup/%s.zip package/%s.zip'%(deviceid,new_package,new_package))
while True:
    try:
        f = zipfile.ZipFile("package/%s.zip" % ( new_package), 'r')
        for file in f.namelist():
            f.extract(file, "package/0" )
        break
    except:
        pass
archive = zipfile.ZipFile('package/%s.zip'%new_package, 'r')
print "%s" % (archive.comment,)
def remove_dir(dir):
   dir = dir.replace('\\', '/')
   if(os.path.isdir(dir)):
       for p in os.listdir(dir):
           remove_dir(os.path.join(dir,p))
       if(os.path.exists(dir)):
           os.rmdir(dir)
   else:
       if(os.path.exists(dir)):
           os.remove(dir)
A16_list=[]
for filename in os.listdir('package/0/0/com.tencent.mm/files/kvcomm/' ):
    try:
        with open('package/0/0/com.tencent.mm/files/kvcomm/%s' % ( filename), 'r') as f:
            A16 = re.findall('(A[0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z][0-9a-z])',f.read())
            if A16 != []:
                A16_list.append(A16[0])
    except:pass
print A16_list
file_list = ['app_tbs','lib']
for i in file_list:
    remove_dir('package/0/0/com.tencent.mm/%s'%i)
shutil.make_archive('package/%s'%(new_package), 'zip', r'package/0')
zf = zipfile.ZipFile('package/%s.zip'%(new_package), 'a')
zf.comment = '011f8828507fc5d303fd51429cfec5d617bed08f2c1b24359657264b6d1094a557ea2e4b558109e42e13278cfc421d173fb003c1ba1a3db2986eb96f2b009e377a691a3276ab2568a4dfe646c75b80f7e6dd8a790929cabf5576312ee560260bd4510b356270cfbf3049ad7b6b9f5b17c24e56cc7ee0433036487d3841e23609'
zf.close()

