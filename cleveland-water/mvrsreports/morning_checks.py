#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MVRS Morning Action Automation Script
Written by Ernest Baker
For any questions or comments, contact: ernest_baker@example.com
"""

import os
import shutil
import time
import smtplib
from datetime import datetime, date, timedelta
from multiprocessing.pool import ThreadPool

# Global message template for notifications
message_template = '''From: MVRS Notification <amrnotificationgroup@example.com>
To: Notification Group <amrnotificationgroup@example.com>
MIME-Version: 1.0
Content-type: text/html
Subject: MVRS Morning Action

<b><center><font size="5">Morning Checks Complete</font></center></b>
'''

def download(download_fail, download_message):
    """
    Handle the download file: copy it to archive, rename it, and modify the global message.
    """
    download_message = download_fail
    download_location = r'E:\Xfer\download\DOWNLOAD.DAT'
    download_attempt = 0

    if date.today().isoweekday() in {6, 7}:  # Skip if weekend
        return f'<br>Today is: {datetime.now().strftime("%A")}<br>There is no download today.<br>'

    while download_attempt < 6:
        if os.path.exists(download_location):
            modified_time = os.path.getmtime(download_location)
            modified_date = date.fromtimestamp(modified_time)
            download_size = os.stat(download_location).st_size >> 10  # Convert size to KB

            if modified_date == date.today():
                shutil.copy2(download_location, r'C:\MVRS\Xfer\DOWNLOAD.DAT')
                shutil.copy2(download_location, modified_date.strftime(r'E:\ARCHIVE\DOWNLOAD\D%Y%m%d.DAT'))
                return f'''
                <br>The DOWNLOAD file was successfully archived, moved, and renamed to:
                <br><a href="\\\\path\\to\\archive\\download">{modified_date.strftime(r'E:\ARCHIVE\DOWNLOAD\D%Y%m%d.DAT')}</a><br>
                The DOWNLOAD size is: {download_size} KB<br>
                '''

            download_attempt += 1
            time.sleep(300)
        else:
            download_attempt += 1
            time.sleep(300)

    return f'''
    <br><font color="#cd2626">The DOWNLOAD file is not in place. Please investigate.
    <br><a href="\\\\path\\to\\download">{download_location}</a></font><br>
    '''

def upload(upload_fail, upload_message):
    """
    Handle the upload file: copy it to archive, rename it, and modify the global message.
    """
    upload_message = upload_fail
    upload_location = r'E:\ARCHIVE\UPLOAD\UPLOAD.DAT'
    upload_attempt = 0

    if date.today().isoweekday() in {1, 7}:  # Skip if Monday or Sunday
        return f'<br>Today is: {datetime.now().strftime("%A")}<br>There was no upload yesterday.<br>'

    while upload_attempt < 6:
        if os.path.exists(upload_location):
            modified_time = os.path.getmtime(upload_location)
            modified_date = date.fromtimestamp(modified_time)
            upload_size = os.stat(upload_location).st_size >> 10  # Convert size to KB

            if modified_date == date.today() - timedelta(1):
                shutil.copy2(upload_location, modified_date.strftime(r'E:\ARCHIVE\UPLOAD\HUL\%Y%m%d.DAT'))
                return f'''
                <br>The UPLOAD file was successfully archived and renamed:
                <br><a href="\\\\path\\to\\archive\\upload\\hul">{modified_date.strftime(r'E:\ARCHIVE\UPLOAD\HUL\%Y%m%d.DAT')}</a><br>
                The UPLOAD size is: {upload_size} KB<br>
                '''

            upload_attempt += 1
            time.sleep(300)
        else:
            upload_attempt += 1
            time.sleep(300)

    return f'''
    <br><font color="#cd2626">The UPLOAD file is not in place. Please investigate.
    <br><a href="\\\\path\\to\\archive\\upload">{upload_location}</a></font><br>
    '''

def dre(dre_fail, dre_message):
    """
    Handle the Daily Route Export (DRE) file: check its existence, modification date, and update the global message.
    """
    dre_message = dre_fail
    dre_location = r'C:\MVRS\FXData\DRE.xml'
    dre_attempt = 0

    while dre_attempt < 6:
        if os.path.exists(dre_location):
            modified_time = os.path.getmtime(dre_location)
            modified_date = date.fromtimestamp(modified_time)
            dre_size = os.stat(dre_location).st_size >> 10  # Convert size to KB

            if modified_date == date.today():
                return f'''
                <br>The DRE is in place with today's date:
                <br><a href="\\\\path\\to\\fxdata">{dre_location}</a><br>
                The DRE size is: {dre_size} KB<br>
                '''

            dre_attempt += 1
            time.sleep(300)
        else:
            dre_attempt += 1
            time.sleep(300)

    return f'''
    <br><font color="#cd2626">The DRE file does not exist:
    <br><a href="\\\\path\\to\\fxdata">{dre_location}</a></font><br>
    '''

def notification(message, download_message, upload_message, dre_message):
    """
    Send the email notification with the results of the morning checks.
    """
    message = message + download_message + upload_message + dre_message
    sender = 'amrnotificationgroup@example.com'
    receivers = 'amrnotificationgroup@example.com'
    
    server = smtplib.SMTP('smtp.example.com', 25)
    server.sendmail(sender, receivers, message)
    server.quit()

def failure(failure_message):
    """
    Send a failure notification if an error occurs.
    """
    sender = 'amrnotificationgroup@example.com'
    receivers = 'amrnotificationgroup@example.com'
    
    server = smtplib.SMTP('smtp.example.com', 25)
    server.sendmail(sender, receivers, failure_message)
    server.quit()

if __name__ == '__main__':
    try:
        pool = ThreadPool(processes=3)
        download_fail = '<br><font color="#cd2626">Download Message Failed</font><br>'
        upload_fail = '<br><font color="#cd2626">Upload Message Failed</font><br>'
        dre_fail = '<br><font color="#cd2626">DRE Message Failed</font><br>'
        
        download_thread = pool.apply_async(download, (download_fail, None))
        upload_thread = pool.apply_async(upload, (upload_fail, None))
        dre_thread = pool.apply_async(dre, (dre_fail, None))
        
        download_message = download_thread.get()
        upload_message = upload_thread.get()
        dre_message = dre_thread.get()
        
        notification(message_template, download_message, upload_message, dre_message)
    except Exception as err:
        failure_message = f'''
        From: MVRS Notification <amrnotificationgroup@example.com>
        To: Notification Group <amrnotificationgroup@example.com>
        MIME-Version: 1.0
        X-Priority: 2
        Content-type: text/html
        Subject: MVRS Morning Action Failure

        <b><center><font size="5">Morning Checks Failed</font></center></b>

        <br><font color="#cd2626">{str(err)}</font><br>
        '''
        failure(failure_message)
