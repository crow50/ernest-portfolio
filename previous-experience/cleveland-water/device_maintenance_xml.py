#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Device Maintenance Automation Script
Written by Ernest Baker
For any questions or comments, contact: ernest_baker@example.com
"""

import time
import pandas as pd
from lxml import etree as ET
import smtplib
import glob
import os
import shutil

# Email message template
message = '''From: Notification System <notificationgroup@example.com>
To: Notification Group <notificationgroup@example.com>
MIME-Version: 1.0
Content-type: text/html
Subject: Device Maintenance

<b><center><font size="5">Device Maintenance Complete</font></center></b>
'''

def dev_maint_process(message):
    """
    Execute Device Maintenance XML generator.
    Data is provided by a SQL query.
    """
    dev_maint = glob.glob(time.strftime(r'\\path\to\DeviceMaintenance\DeviceMaintenance%Y%m%d*.csv'))
    checks = 1

    while len(dev_maint) == 0:
        if checks == 30:
            dev_maint_message = '<br>The Device Maintenance file is not in place.<br>'
            notification(message, dev_maint_message)
            quit()
        checks += 1
        time.sleep(30)

    if os.path.exists(dev_maint[-1]):
        try:
            dev_maint_file = pd.read_csv(dev_maint[-1])
            root = ET.Element("DeviceMaintenance", xmlns="http://www.itron.com/ItronInternalImportXsd/2.0")

            for index, row in dev_maint_file.iterrows():
                SetDevice = ET.SubElement(root, 'SetDevice', Active='true', ChannelNumber='1', 
                                          DeviceType=str(row[1]), DeviceId=str(row[0]))
                ET.SubElement(SetDevice, 'SetAddress', Longitude=str(row[10]), Latitude=str(row[9]), 
                              Zip=str(row[8]), Country="USA", State="OH", City=str(row[5]), 
                              StreetAddress=str(row[4]))
                ET.SubElement(SetDevice, 'SetDeviceGroup', DeviceGroup=str(row[11]), DeviceGroupType="ROUTE")
                ET.SubElement(SetDevice, 'SetReference', Meter=str(row[15]), Account=str(row[14]), 
                              Premise=str(row[13]))
                ET.SubElement(SetDevice, 'SetDecodeType', DecodeType=str(row[16]))

            tree = ET.ElementTree(root)
            tree.write(time.strftime("%Y%m%d_dev_add_maint_automatically_generated.xml"), pretty_print=True)

        except pd.errors.EmptyDataError:
            print('No data')
            dev_maint_message = '<br>The Device Maintenance File is empty.<br>'
            error_message = '''From: Notification System <notificationgroup@example.com>
To: Notification Group <notificationgroup@example.com>
MIME-Version: 1.0
X-Priority: 2
Content-type: text/html
Subject: Device Maintenance Error

<b><center><font size="5">Device Maintenance Error</font></center></b>
            '''
            notification(error_message, dev_maint_message)
    
    time.sleep(30)
    dev_maint_archive(message, dev_maint_file)

def dev_maint_archive(message, dev_maint_file):
    """
    Archive or handle failure of Device Maintenance process.
    """
    successful_archive = glob.glob(time.strftime(r"\\path\to\Archive\%Y%m%d_dev_add_maint_automatically_generated*"))
    failed_archive = glob.glob(time.strftime(r"\\path\to\Errors\%Y%m%d_dev_add_maint_automatically_generated*"))

    check = 1
    while len(successful_archive) == 0 and len(failed_archive) == 0:
        time.sleep(30)
        if check == 30:
            dev_maint_message = '<br>It has been 15 minutes and the device file has not been moved.<br>'
            error_message = '''From: Notification System <notificationgroup@example.com>
To: Notification Group <notificationgroup@example.com>
MIME-Version: 1.0
X-Priority: 2
Content-type: text/html
Subject: Device Maintenance Error

<b><center><font size="5">Device Maintenance Error</font></center></b>
            '''
            notification(error_message, dev_maint_message)

    if os.path.exists(successful_archive[-1]):
        dev_maint_message = f'<br>The Device Maintenance file was successfully loaded.<br><br>There are: {len(dev_maint_file.index)} devices.<br>'
        notification(message, dev_maint_message)
    elif os.path.exists(failed_archive[-1]):
        dev_maint_message = '<br>The Device Maintenance file failed. The XML file is located in the error folder.<br>'
        notification(message, dev_maint_message)
    
    # NOTE: Uncomment this before scheduling
    # shutil.copy2(dev_maint, time.strftime(r'\\path\to\Archive\%Y\%m\DeviceMaintenance%Y%m%d.csv'))

def notification(message, dev_maint_message):
    """
    Send an email notification with the provided message.
    """
    message = message + dev_maint_message
    sender = 'notificationgroup@example.com'
    receivers = 'notificationgroup@example.com'
    server = smtplib.SMTP('smtp.example.com', 25)
    server.sendmail(sender, receivers, message)
    server.quit()

if __name__ == '__main__':
    try:
        dev_maint_process(message)
    except Exception as e:
        notification(message, dev_maint_message=str(e))
