import sys
import os
import socket
import mysql.connector
from datetime import datetime
import smtplib, ssl
from datetime import datetime

mailAddress = 'srv.schneg@gmail.com'
mailPassw = 'sicheresPasswort123'

ip_arduino = '192.168.1.104'
port_arduino = 4711


mydb = mysql.connector.connect(
    port=3333,
    host="srv-schneg",
    user="root",
    password="sicheresPasswort123",
    db="Notification"
)

def sendMail(mailTo, mailSubject, mailText):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(mailAddress, mailPassw)
        server.sendmail(mailAddress, mailTo, "Subject:Problem mit Dienst!\n" + mailText)

def testArduinoUp():


    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip_arduino, port_arduino))
        s.settimeout(10)
        msgToSend = 'do:howMuchWater?'
        s.send(msgToSend.encode('utf-8'))
        rcv = s.recv(1024).decode()
        s.close()
        print ("Arduino is UP")
    except:
        print("Arduino is DOWN")
        sqlserver = mydb.cursor()
        sqlserver.execute("SELECT * FROM emailNotification WHERE RainSys_arduinoDown = true")
        for row in sqlserver.fetchall():
            dateTimeObj = datetime.now()
            sendMail(row[0], 'Arduino offline', 'Konnte den Bewaesserungs-Arduino nicht erreichen! \n\nTimestamp:' + dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)"))


if __name__ == '__main__':
    testArduinoUp()