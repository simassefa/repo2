# !/usr/bin/python

###########################################################
#
# This python script is used for sending Consolidation email
#
# Written by : simret Demissies
# Created date: 4/18/2022

# Last modified:
# Tested with : Python 3.6.8

# Script Revision: 1.0
#
##########################################################


from mysql_daily_backup import backup_mysql
from prometheus_backup import backup_prometheus

import smtplib
import pandas
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
copy_Backup = 'XX.X.X.X:/home/prometheus-snapshots/'

def send_email(mysql_backup_list, prometheus_backup_file):
    #prometheus backup html format
    PromBackup = [{'backup file': prometheus_backup_file, 'status': 'success', 'copy_Backup':
        prometheus_backup_file.replace('''/var/lib/prometheus/snapshots/''', copy_Backup)}]
    print('backup data: ', PromBackup)
    df = pandas.DataFrame(PromBackup)
    print(df)
    prometheus_text_table = df.to_string()
    prometheus_html_table = df.to_html(index=False)

    #mysql backup html format
    df = pandas.DataFrame(mysql_backup_list).reindex(
        columns=['database_name', 'status', 'backup_file', 'copy_backup']
    )
    mysql_text_table = df.to_string()

    mysql_html_table = df.to_html(index=False)
    html = """
           <html>
           <head>
           <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
           <title>Backup report</title>
           <style type="text/css" media="screen">
           table, th, td{
             border: 1px solid black;
             border-collapse: collapse;
            }
            th, td {
             padding: 16px;
           }
           </style>
           </head>
           <body>
           <p style="background-color:powderblue; display: inline-flex;padding: 3px;font-size: 24px;">MySql Backup Report:</p>
           <p></p>
           <a href="https://gyan.5gaas.tech:3000/d/M_5qKzy7z/mysql-overview-percona-app?orgId=1&viewPanel=63&from=now-2d&to=now">MySql Backup Dashboard<br/></a>
           <p></p>
           
           %s
           <p style="background-color:powderblue; display: inline-flex;padding: 3px;font-size: 24px;">Prometheus Backup Report:</p>
           <a href="https://gyan.5gaas.tech:3000/d/D-Cf0b87k/prometheus-monitoring-dashboard-ssoc?orgId=1&viewPanel=18&from=now-2d&to=now">Prometheus Backup Dashboard <br/></a>
       
           
           %s
           <p>If there are any issues that require immediate attention,Please contact Al ops / ai_ops@betacom.com,</p>
           <p></p>
           </body></html>
           """

    html = html % (mysql_html_table, prometheus_html_table)
    text_table = mysql_text_table + prometheus_text_table

    message = MIMEMultipart(
        "alternative", None, [MIMEText(text_table), MIMEText(html, 'html')])

    message['Subject'] = "Consolidation Backup status Report on BETAZR01ZAB001"

    to_list = ['users','uses']
    conn = smtplib.SMTP('mail.privateemail.com', 587)
    type(conn)
    conn.ehlo()
    conn.starttls()
    conn.login('userName', 'password')
    conn.sendmail('ssoc@XXXX.tech', to_list, message.as_string())
    conn.quit()


mysql = backup_mysql()
prometheus = backup_prometheus()
send_email(mysql, prometheus)

