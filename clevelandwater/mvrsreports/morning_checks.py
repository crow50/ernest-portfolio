# -*- coding: utf-8 -*-
#!/usr/bin/env python3
#Written in Python3.7 by Ernest Baker. If you have any questions or comments, email me at ernest_baker@clevelandwater.com


import os
import shutil
import datetime
import time
import smtplib
import queue
from datetime import datetime,date,timedelta
from multiprocessing.pool import ThreadPool


#Global message that is sent
message = '''From: AMRMVRSPROD <amrnotificationgroup@clevelandwater.com>
To: AMR Notification Group <amrnotificationgroup@clevelandwater.com>
MIME-Version: 1.0
Content-type: text/html
Subject: MVRS Morning Action

<b><center><font size="5">Morning Checks Complete</font></center></b>

'''


def download(download_fail,download_message):
    '''
    This function is for the download file.
    It copies it to archive, renames it, and modifies the corresponding global message
    '''
    download_message = download_fail
    download_location = r'E:\Xfer\download\DOWNLOAD.DAT'
    download_attempt = 0
    if date.today().isoweekday() in {6,7}:
        upload_message = '<br>Today is: ' + datetime.strftime(datetime.now(),'%A') + '<br>' + 'There is no download today.' + '<br>'
        return upload_message
    while download_attempt < 6:
        if os.path.exists(download_location) is True:
            modified_time = os.path.getmtime(download_location)
            modified_date = date.fromtimestamp(modified_time)
            download_size = os.stat(download_location).st_size >> 10
            while download_attempt < 6:
                if modified_date == date.today():
                    shutil.copy2(r'E:\Xfer\download\DOWNLOAD.DAT', r'C:\MVRS\Xfer\DOWNLOAD.DAT')
                    shutil.copy2(r'E:\Xfer\download\DOWNLOAD.DAT', modified_date.strftime(r'E:\ARCHIVE\DOWNLOAD\D%Y%m%d.DAT'))
                    download_message = '<br>The DOWNLOAD file was successfully archived, moved and renamed to: '+ '<br>' + '<a href="\\\\amrmvrsprod\\e\\archive\\download">' + modified_date.strftime(r'E:\ARCHIVE\DOWNLOAD\D%Y%m%d.DAT') + '</a>' + '<br>' + 'The DOWNLOAD size is: ' + str(download_size) + ' KB' + '<br>'
                    return download_message
                time.sleep(300)
                download_attempt += 1
            download_message = '<br><font color="#cd2626">The DOWNLOAD file is in place but it does not have today\'s date: '+ '<br>' + str(modified_date) + '<br>' + '<a href="\\\\amrmvrsprod\\xfer\\download">' + str(download_location) +'</a>' + '</font><br>'
            return download_message
        time.sleep(300)
        download_attempt += 1
    download_message = '<br><font color="#cd2626">The DOWNLOAD file is not in place. Please investigate.' + '<br>' + '<a href="\\\\amrmvrsprod\\xfer\\download">' + str(download_location) + '</a>' + '</font><br>'
    return download_message


def upload(upload_fail,upload_message):
    '''
    This function is for the upload file.
    It copies it to archive, renames it, and modifies the corresponding global message
    '''
    upload_message = upload_fail
    upload_location = r'E:\ARCHIVE\UPLOAD\UPLOAD.DAT'
    upload_attempt = 0
    if date.today().isoweekday() in {1,7}:
        upload_message = '<br>Today is: ' + datetime.strftime(datetime.now(),'%A') + '<br>' + 'There was no upload yesterday.' + '<br>'
        return upload_message
    while upload_attempt < 6:
        if os.path.exists(upload_location) is True:
            modified_time = os.path.getmtime(upload_location)
            modified_date = date.fromtimestamp(modified_time)
            upload_size = os.stat(upload_location).st_size >> 10
            while upload_attempt < 6:
                if modified_date == date.today() - timedelta(1):
                    shutil.copy2(r'E:\ARCHIVE\UPLOAD\UPLOAD.DAT', modified_date.strftime(r'E:\ARCHIVE\UPLOAD\HUL\%Y%m%d.DAT'))
                    upload_message = '<br>The UPLOAD file was successfully archived and renamed: ' + '<br>' + '<a href="\\\\amrmvrsprod\\e\\archive\\upload\\hul">' + modified_date.strftime(r'E:\ARCHIVE\UPLOAD\HUL\%Y%m%d.DAT') + '</a>' ' <br>' + 'The UPLOAD size is: ' + str(upload_size) + ' KB' + '<br>'
                    return upload_message
                time.sleep(300)
                upload_attempt += 1
            upload_message = '<br><font color="#cd2626">The UPLOAD file does not have the correct date:'+'<br>'+ str(modified_date) + '<br>' + '<a href="\\\\amrmvrsprod\\e\\archive\\upload">' + str(upload_location) + '</a>' + '</font><br>'
            return upload_message
        time.sleep(300)
        upload_attempt += 1
    upload_message = '<br><font color="#cd2626">The UPLOAD file is not in place. Please investigate.' + '<br>' + '<a href="\\\\amrmvrsprod\\e\\archive\\upload">' + str(upload_location) + '</a>' '</font><br>'
    return upload_message


def dre(dre_fail,dre_message):
    '''
    This is for the DRE or Daily Route Export.
    It is written in a while loop.
    It sees if the DRE exists first.
    If it does, then it continues to check if it was modified today.
    If it does not exist, it loops five minutes at a time.
    If it was, then it modifies the dre_message variable.
    If it was not modified today, it still modifies the dre_message, but with different wording.
    '''
    dre_message = dre_fail
    dre_location = r'C:\MVRS\FXData\DRE.xml'
    dre_attempt = 0
    while dre_attempt < 6:
        if os.path.exists(dre_location) is True:
            modified_time = os.path.getmtime('C:\MVRS\FXData\DRE.xml')
            modified_date = date.fromtimestamp(modified_time)
            dre_size = os.stat(r'C:\MVRS\FXData\DRE.xml').st_size >> 10
            while dre_attempt < 6:
                if modified_date == date.today():
                    dre_message = '<br>The DRE is in place with todays date: ' + '<br>' + '<a href="\\\\amrmvrsprod\\c\\mvrs\\fxdata">' + str(dre_location) + '</a>' + '<br>' + str(modified_date) + '<br>' + 'The DRE size is: ' + str(dre_size) + ' KB' + '<br>'
                    return dre_message
                time.sleep(300)
                dre_attempt+=1
            dre_message = '<br><font color="#cd2626">The DRE is in place, but it has the wrong date: ' + '<br>' + str(modified_date) + '<br>' + '<a href="\\\\amrmvrsprod\\c\\mvrs\\fxdata">' + str(dre_location) + '</a>' + '</font><br>'
            return dre_message
        time.sleep(300)
        dre_attempt+=1
    dre_message = '<br><font color="#cd2626">The DRE file does not exist: ' + '<br>' + '<a href="\\\\amrmvrsprod\\c\\mvrs\\fxdata">' + str(dre_location) + '</a>' + '</font><br>'
    return dre_message


def notification(message,download_message,upload_message,dre_message):
    message = message + download_message + upload_message + dre_message
    sender = 'amrnotificationgroup@clevelandwater.com'
    receivers = 'amrnotificationgroup@clevelandwater.com'
    server = smtplib.SMTP('ex2013cas1.clevelanddpu.org', 25)
    server.sendmail(sender, receivers, message)
    server.quit()


def failure(failure_message):
    sender = 'amrnotificationgroup@clevelandwater.com'
    receivers = 'amrnotificationgroup@clevelandwater.com'
    server = smtplib.SMTP('ex2013cas1.clevelanddpu.org', 25)
    server.sendmail(sender, receivers, failure_message)
    server.quit()


if __name__ == '__main__':
    try:
        pool = ThreadPool(processes=3)
        download_message = None
        upload_message = None
        dre_message = None
        download_fail = '<br><font color="#cd2626">Download Message Failed</font><br>'
        upload_fail = '<br><font color="#cd2626">Upload Message Failed</font><br>'
        dre_fail = '<br><font color="#cd2626">DRE Message Failed</font><br>'
        download_thread = pool.apply_async(download, (download_fail,download_message))
        upload_thread = pool.apply_async(upload, (upload_fail,upload_message))
        dre_thread = pool.apply_async(dre, (dre_fail, dre_message))
        download_message = download_thread.get()
        upload_message = upload_thread.get()
        dre_message = dre_thread.get()
        notification(message,download_message,upload_message,dre_message)
    except Exception as err:
        message = '''From: AMRMVRSPROD <amrnotificationgroup@clevelandwater.com>
To: AMR Notification Group <amrnotificationgroup@clevelandwater.com>
MIME-Version: 1.0
X-Priority: 2
Content-type: text/html
Subject: MVRS Morning Action Failure

<b><center><font size="5">Morning Checks Failed</font></center></b>

'''
        failure_message = message + '<br><font color="#cd2626">' + str(err) + '</font><br>'
        failure(failure_message)
