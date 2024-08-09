#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MVRS Evening Upload Automation Script
Written by Ernest Baker
For any questions or comments, contact: amrnotificationgroup@example.com
"""

import os
import shutil
import time
import smtplib
from datetime import datetime, date, timedelta

def upload():
    """
    Handle the upload process for the MVRS evening checks.
    """
    upload_message = '<br><font color="#cd2626">Upload Message Failed</font><br>'
    upload_location = r'C:\MVRS\Xfer\Upload\UPLOAD.DAT'
    upload_attempt = 0

    if date.today().isoweekday() in {6, 7}:  # Skip if weekend
        upload_message = '<br>Today is: ' + datetime.strftime(datetime.now(), '%A') + '<br>' + 'There is no upload today.'
        return upload_message

    while upload_attempt < 6:
        if os.path.exists(upload_location):
            modified_time = os.path.getmtime(upload_location)
            modified_date = date.fromtimestamp(modified_time)
            upload_size = os.stat(upload_location).st_size >> 10  # Convert size to KB

            while upload_attempt < 6:
                if modified_date == date.today():
                    shutil.copy2(upload_location, r'E:\Xfer\Upload\UPLOAD.DAT')
                    shutil.move(upload_location, r'E:\Archive\Upload\UPLOAD.DAT')
                    upload_message = f'''
                    <br>The UPLOAD file was successfully copied and moved: 
                    <br>Copied to: <a href="\\\\path\\to\\upload">E:\Xfer\Upload\UPLOAD.DAT</a><br>
                    Moved to: <a href="\\\\path\\to\\upload">E:\Archive\Upload\UPLOAD.DAT</a><br>
                    <br>The UPLOAD size is: {upload_size} KB<br>
                    '''
                    return upload_message

                time.sleep(300)
                upload_attempt += 1

            upload_message = f'''
            <br><font color="#cd2626">The UPLOAD file does not have the correct date:
            <br>{modified_date}<br><a href="\\\\path\\to\\upload">{upload_location}</a></font><br>
            '''
            return upload_message

        time.sleep(300)
        upload_attempt += 1

    upload_message = f'''
    <br><font color="#cd2626">The UPLOAD file is not in place. Please investigate.
    <br><a href="\\\\path\\to\\upload">{upload_location}</a></font><br>
    '''
    return upload_message

def notification(upload_message):
    """
    Send an email notification after the upload process.
    """
    message = '''From: MVRS Notification <amrnotificationgroup@example.com>
To: Notification Group <amrnotificationgroup@example.com>
CC: Team <team@example.com>
MIME-Version: 1.0
Content-type: text/html
Subject: MVRS Evening Upload Action

<b><center><font size="5">Evening Checks Complete</font></center></b>
'''
    sender = 'amrnotificationgroup@example.com'
    to = 'amrnotificationgroup@example.com'
    cc = ['team@example.com']
    receivers = [to] + cc
    message += upload_message

    server = smtplib.SMTP('smtp.example.com', 25)
    server.sendmail(sender, receivers, message)
    server.quit()

def failure(failure_message):
    """
    Send an email notification in case of a failure.
    """
    sender = 'amrnotificationgroup@example.com'
    receivers = 'amrnotificationgroup@example.com'
    server = smtplib.SMTP('smtp.example.com', 25)
    server.sendmail(sender, receivers, failure_message)
    server.quit()

try:
    upload_message = upload()
    notification(upload_message)
except Exception as err:
    message = '''From: MVRS Notification <amrnotificationgroup@example.com>
To: Notification Group <amrnotificationgroup@example.com>
MIME-Version: 1.0
X-Priority: 2
Content-type: text/html
Subject: MVRS Evening Action Failure

<b><center><font size="5">Evening Checks Failed</font></center></b>
'''
    failure_message = f'{message}<br><font color="#cd2626">{str(err)}</font><br>'
    failure(failure_message)
