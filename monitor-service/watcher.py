import sys
import time
import logging
import getpass
import os
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import xml.etree.cElementTree as ET
import sqlite3
import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class DataContainer():
    def __init__(self, parent=None):
        self.db = sqlite3.connect('logs.dat')
        self.cursor = self.db.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS log(id INTEGER PRIMARY KEY, message TEXT,
                               time TEXT, action TEXT)
        ''')
        self.db.commit()

    def initModels(self):
        return True


class EventHandler(LoggingEventHandler):

    def on_moved(self, event):
            super(LoggingEventHandler, self).on_moved(event)
            what = 'directory' if event.is_directory else 'file'
            message = "Moved "+what+": from "+event.src_path+" to "+event.dest_path
            pTime = time.strftime("%m-%d-%Y %H:%M%p")
            action = "MOVE"
            self.send_data(message, pTime, action)
            #logging.info("Moved %s: from %s to %s, by %s", what, event.src_path, event.dest_path, getpass.getuser())

    def on_created(self, event):
            super(LoggingEventHandler, self).on_created(event)
            what = 'directory' if event.is_directory else 'file'
            message = "Created "+what+": " + event.src_path
            pTime = time.strftime("%m-%d-%Y %H:%M%p")
            action = "CREATE"
            self.send_data(message, pTime, action)
            #logging.info("Created %s: %s, by %s", what, event.src_path, getpass.getuser())

    def on_deleted(self, event):
            super(LoggingEventHandler, self).on_deleted(event)
            what = 'directory' if event.is_directory else 'file'
            message = "Deleted "+what+": "+event.src_path
            pTime = time.strftime("%m-%d-%Y %H:%M%p")
            action = "DELETE"
            self.send_data(message, pTime, action)
            #logging.info("Deleted %s: %s, by %s", what, event.src_path, getpass.getuser())

    def on_modified(self, event):
            super(LoggingEventHandler, self).on_modified(event)
            what = 'directory' if event.is_directory else 'file'
            message = "Modified " + what + ": " + event.src_path
            pTime = time.strftime("%m-%d-%Y %H:%M%p")
            action = "MODIFY"
            self.send_data(message, pTime, action)
            #logging.info("Modified %s: %s, by %s", what, event.src_path, getpass.getuser())

    def send_data(self, message, time, action):
        data = DataContainer()
        data.cursor = data.db.cursor()
        data.cursor.execute('''
                insert into log(message, time, action) values(\''''+ message +'''\',\''''+time+'''\',\''''+action+'''\')
            ''')
        data.db.commit()

        print(message + " : " + time) #test

    #def getUser(self, filename):
    #    return getpwuid(stat(filename).st_uid).pw_name

class Config():
    def readConfigurations(self):
        if os.path.exists('../monitor-server/client-config.xml'): #test
            self.path = '../monitor-server/client-config.xml'
            root = ET.parse(self.path).getroot()
        elif os.path.exists('../client-config.xml'): #build
            self.path = '../client-config.xml'
            root = ET.parse(self.path).getroot()
        else:#co config yet
            return False

        readPaths = []
        for paths in root:
            if paths.tag == "paths":
                for path in paths:
                    readPaths.append(path.text)

        return readPaths

    def sendNotification(self):
        data = DataContainer()
        data.cursor = data.db.cursor()
        
        timestamp = time.strftime("%m-%d-%Y")
        data.cursor.execute('''select * from log where substr(time,0,11)=\'''' + timestamp + '''\'''')
        
        cr = data.cursor.fetchall()

        message = '''
            <table style='border-spacing: 0;'>
                <tr>
                    <th style='border: solid #000 1px;padding: 2px 10px;'>Log</th>
                    <th style='border: solid #000 1px;padding: 2px 10px;'>Time</th>
                    <th style='border: solid #000 1px;padding: 2px 10px;'>Event</th>
                </tr>
        '''
        for row in cr:

           message = message + '''
                <tr>
                    <td style='border: solid #000 1px;padding: 2px 10px;'>''' + row[1] + '''</td>
                    <td style='border: solid #000 1px;padding: 2px 10px;'>''' + row[2] + '''</td>
                    <td style='border: solid #000 1px;padding: 2px 10px;'>''' + row[3] + '''</td>
                </tr>
           '''

        message = message + "</table>"

        self.writeLog(message)
        print("log has been saved to disk...")
        data.db.close()

        print("Extracting configuration...")
        root = ET.parse(self.path).getroot()
        #doc = ET.SubElement(root, "SMTP")

        for doc in root:
            if doc.tag == "smtp":
                for smtp in doc:
                    if smtp.tag == "server":
                        smtpServer = str(smtp.text)
                    if smtp.tag == "port":
                        smtpPort = str(smtp.text)
                    if smtp.tag == "username":
                        username = str(smtp.text)
                    if smtp.tag == "password":
                        password = str(smtp.text)
                    if smtp.tag == "auth":
                        auth = True if smtp.text == 'True' else False

                    if smtp.tag == "emails":
                        for emails in smtp:
                            print("Sending email to " + str(emails.text) + "...")
                            self.sendEmail(smtpServer, smtpPort, username, password, emails.text, "OpenMonitor Report", message, True)


    def writeLog(self, message):
        
        timestamp = time.strftime("%m-%d-%Y")

        if not os.path.exists("./logs/"):
            os.makedirs("./logs/")


        #write file
        file = open("./logs/" + timestamp + ".html","w") 
         
        file.write(message) 
         
        file.close() 

    def sendEmail(self, server, port, username, password,toEmail, subject, message, allowAuth):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = "Open Monitor"
        msg['To'] = toEmail
        msg.attach(MIMEText(message, 'html'))

        server = smtplib.SMTP(server, port)
        server.ehlo()
        server.starttls()
        server.ehlo()

        if allowAuth:
            server.login(username, password)

        server.sendmail(username, toEmail, msg.as_string())
        server.quit()

                    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    event_handler = EventHandler()
    threads = []
    observer = Observer()
    config = Config()
    paths = config.readConfigurations()

    #config.sendNotification()

    if paths == False:
        print("No config file! Create a config file using the GUI")
    else:
        data = DataContainer()
        
        for path in paths:
            observer.schedule(event_handler, path, recursive=True)
            threads.append(observer)

        observer.start()
        try:
            while True:
                if (time.strftime("%H:%M:%S") == "23:59:59"): #busy..will come back to this
                    config.sendNotification()
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
