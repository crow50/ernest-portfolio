#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Route Status Report Automation Script
Written by Ernest Baker
For any questions or comments, contact: ernest_baker@example.com
"""

import pandas as pd
from datetime import date
import time
import os
import glob
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

# Load the billing calendar
billcal = pd.read_excel('BillCalendar.xlsx')
bill_cycle = billcal.loc[:, ['Monthly Billing', 'Cycle', date.today().strftime('%B')]].set_index(
    str(date.today().strftime('%B'))).filter(like=time.strftime('%Y-%m-%d'), axis=0)


def rstat_creation(bill_cycle):
    """
    Create the RSTAT report based on the billing cycle.
    """
    cycle_count = 0
    writer_mode = 'w'
    while len(bill_cycle.index) > cycle_count:
        cycle = bill_cycle.loc[:, 'Cycle'].values[cycle_count]
        mb_cycle = bill_cycle.loc[:, 'Monthly Billing'].values[cycle_count]
        with open('RSTAT.csv', 'w') as f:
            rstat = glob.glob(r'\\path\to\Reports\RSTAT*.txt')
            rstat = open(''.join(rstat[-1]), 'r').readlines()
            for line in rstat:
                if line.startswith(' ' + str(cycle)):
                    f.write(" ".join(line.split()).replace(' ', ','))
                    f.write("\n")
            f.close()

        header = ['Route', 'Start Date', 'End Date', 'Reads Requested', 'Reads Received', 'Reads Missed', 'Reads Skipped', 'Percentage Read']
        rstat = pd.read_csv('RSTAT.csv', names=header)
        rstat.drop(['Start Date', 'End Date', 'Reads Skipped', 'Percentage Read'], axis=1, inplace=True)

        total = pd.DataFrame({'Route': [str(mb_cycle) + ' Totals'], 'Reads Requested': [rstat['Reads Requested'].sum()], 
                              'Reads Received': [rstat['Reads Received'].sum()], 'Reads Missed': [rstat['Reads Missed'].sum()]})
        amr = rstat[rstat['Route'].str.contains('A|B|C')]
        amr_reads = pd.DataFrame({'Route': [str(mb_cycle) + ' AMR Totals'], 'Reads Requested': [amr['Reads Requested'].sum()], 
                                  'Reads Received': [amr['Reads Received'].sum()], 'Reads Missed': [amr['Reads Missed'].sum()]})
        non_amr = rstat[rstat['Route'].str.contains('A|B|C') == False]
        non_amr_reads = pd.DataFrame({'Route': [str(mb_cycle) + ' Non-AMR Totals'], 'Reads Requested': [non_amr['Reads Requested'].sum()], 
                                      'Reads Received': [non_amr['Reads Received'].sum()], 'Reads Missed': [non_amr['Reads Missed'].sum()]})
        rstat = pd.concat([rstat, total, amr_reads, non_amr_reads], ignore_index=True)

        try:
            rstat['Percentage Read'] = rstat['Reads Received'] / rstat['Reads Requested']
        except ZeroDivisionError:
            rstat['Percentage Read'] = 0

        rstat['Percentage Read'].fillna(0, inplace=True)
        rstat['Percentage Read'] = pd.Series(["{0:.2f}%".format(val * 100) for val in rstat['Percentage Read']], index=rstat.index)

        with pd.ExcelWriter(time.strftime(r'\\path\to\Reports\%Y%m%dRouteStatusReport.xlsx'), mode=writer_mode, engine='openpyxl') as writer:
            rstat.to_excel(writer, sheet_name=str(mb_cycle), index=False)

        os.remove('RSTAT.csv')
        cycle_count += 1
        writer_mode = 'a'


def totals():
    """
    Generate the grand totals from the route status reports.
    """
    xls = pd.ExcelFile(time.strftime(r'\\path\to\Reports\%Y%m%dRouteStatusReport.xlsx'))
    sheet_count = 0
    totals_df = pd.DataFrame([])

    while sheet_count < len(bill_cycle.index):
        sheet = pd.read_excel(xls, sheet_name=sheet_count).tail(3)
        totals_df = pd.concat([totals_df, sheet], ignore_index=True)
        sheet_count += 1

    amr = totals_df[totals_df['Route'].str.contains('Non') == False]
    amr = amr[amr['Route'].str.contains('AMR') == True]
    amr_reads = pd.DataFrame({'Route': ['AMR Grand Totals'], 'Reads Requested': [amr['Reads Requested'].sum()], 
                              'Reads Received': [amr['Reads Received'].sum()], 'Reads Missed': [amr['Reads Missed'].sum()]})

    non_amr = totals_df[totals_df['Route'].str.contains('Non-AMR') == True]
    non_amr_reads = pd.DataFrame({'Route': ['Non-AMR Grand Totals'], 'Reads Requested': [non_amr['Reads Requested'].sum()], 
                                  'Reads Received': [non_amr['Reads Received'].sum()], 'Reads Missed': [non_amr['Reads Missed'].sum()]})

    totals = totals_df[totals_df['Route'].str.contains('Non-AMR|AMR') == False]
    totals_reads = pd.DataFrame({'Route': ['Grand Totals'], 'Reads Requested': [totals['Reads Requested'].sum()], 
                                 'Reads Received': [totals['Reads Received'].sum()], 'Reads Missed': [totals['Reads Missed'].sum()]})

    totals_df = pd.concat([totals_df, amr_reads, non_amr_reads, totals_reads], ignore_index=True, sort=False)

    try:
        totals_df['Percentage Read'] = totals_df['Reads Received'] / totals_df['Reads Requested']
    except ZeroDivisionError:
        totals_df['Percentage Read'] = 0

    totals_df['Percentage Read'].fillna(0, inplace=True)
    totals_df['Percentage Read'] = pd.Series(["{0:.2f}%".format(val * 100) for val in totals_df['Percentage Read']], index=totals_df.index)

    with pd.ExcelWriter(time.strftime(r'\\path\to\Reports\%Y%m%dRouteStatusReport.xlsx'), mode='a', engine='openpyxl') as writer:
        totals_df.to_excel(writer, sheet_name='Grand Totals', index=False)


def send_mail():
    """
    Send the route status report via email.
    """
    rstat = time.strftime(r'\\path\to\Reports\%Y%m%dRouteStatusReport.xlsx')
    text = 'All,<br>Here is the Route Status Report for today.'
    send_from = 'notificationgroup@example.com'
    send_to = 'notificationgroup@example.com'

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = time.strftime(r'%Y%m%dRouteStatusReport')
    msg.attach(MIMEText(text))

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(rstat, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename=RouteStatusReport.xlsx')
    msg.attach(part)

    smtp = smtplib.SMTP('smtp.example.com', 25)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()


if __name__ == '__main__':
    if bill_cycle.index.empty:
        print("No cycles selected for reading. Is today a skip day?")
        time.sleep(30)
        quit()

    try:
        if date.today().isoweekday() in {6, 7}:  # Skip if weekend
            quit()
        else:
            rstat_creation(bill_cycle)
            if len(bill_cycle.index) != 1:
                totals()
            send_mail()
    except Exception as err:
        print(str(err))
