from PyQt4 import uic
from PyQt4 import QtCore
from PyQt4 import QtGui
from functools import partial
from frmLogin import frmLogin
import datetime
import sched,time
import mp3play


#from time import strftime,strptime


( Ui_MainWindow, QMainWindow ) = uic.loadUiType( 'mainwindow.ui' )

class Alarm_Thread(QtCore.QThread):
    def __init__(self,mwwindow):
        #Mainwindow and all form components pass to
        QtCore.QThread.__init__(self,mwwindow)
        
        self.mwwindow = mwwindow
        self.test = 1
        self.alarm =[]
        self.alarm_hourly = []
      


    def run(self):
        # Run scheduler thread
        s = sched.scheduler(time.time, time.sleep)
        s.enter(1, 1, self.check_timeAlarm, (s,))
        s.run()


    def check_timeAlarm(self,sc):
      
        
        for set_alarm in self.alarm:
            
            C_time = datetime.datetime.now().time()
            #print "Set Alarm: "+str(set_alarm) + " ### " + str(C_time.strftime("%I:%M %p"))
            if str(set_alarm) == C_time.strftime("%I:%M %p"):
                self.mwwindow.ui.text_display.append("***** Alarm Shift *****")
                ## Call play sounds
                self.filename = r'chime_music.mp3'
                self.clip = mp3play.load(self.filename)
                self.clip.play()
                time.sleep(80)
                self.clip.stop()
                self.mwwindow.ui.text_display.moveCursor(QtGui.QTextCursor.End)

            else:
                for set_hourly in self.alarm_hourly:
                    #print "Set Alarm: "+str(set_alarm)+" ### "+C_time.strftime("%I:%M %p")
                    C_time = datetime.datetime.now().time()
                    #print set_hourly + " #### " + C_time.strftime("%I:%M %p")
                    if str(set_hourly) == C_time.strftime("%I:%M %p"):
                        self.mwwindow.ui.text_display.append("***** Exercise Sounds *****")
                        self.filename = r'Exercise_music.mp3'
                        
                        ## Call play sounds
                        self.clip = mp3play.load(self.filename)
                        self.clip.play()
                        time.sleep(80)
                        self.clip.stop()
                        self.mwwindow.ui.text_display.moveCursor(QtGui.QTextCursor.End)
                        

        sc.enter(1, 1, self.check_timeAlarm, (sc,))

    def stop(self):
        print 'Closing Chime'
        try:
            self.w.destroy()
        except:
            pass
        self.terminate()

class MainWindow ( QMainWindow ):
    """MainWindow inherits QMainWindow"""

    def __init__ ( self, parent = None ):
        QMainWindow.__init__( self, parent )
        self.ui = Ui_MainWindow()
        self.ui.setupUi( self )
        self.thread  = Alarm_Thread(self)
        self.Password_Holder=""
      
        
        
        #Initialize label display
        #C_Date_Time = datetime.datetime.now()
        #self.ui.lbl_CurrentDate.setText(C_Date_Time.strftime("%A, %d. %B %Y"))
        #self.ui.lbl_CurrentTime.setText("")
        
        #Update Time button is clicked
        #self.ui.btn_Start.clicked.connect(self.AddTime)
        
        
        #Confirm Password is clicked
        self.ui.btn_Pass.clicked.connect(self.CheckPass)
        
        
        
        #Hide frmPassword
        self.ui.frmPassword.setVisible(False)
           
           
        ##################### Forms and TextDisplay Design #################
        pal = QtGui.QPalette()
        bgc = QtGui.QColor(0, 0, 0)
        textc = QtGui.QColor(0, 254, 29)
        
        #Qtext Backgruond color
        pal.setColor(QtGui.QPalette.Base, bgc)
        #Qtext Backgruond color
        pal.setColor(QtGui.QPalette.Text, textc)  
        self.ui.text_display.setPalette(pal)
   
        
        self.AddTime()
           
           
           
    def __del__ ( self ):
        self.ui = None
        
    def closeEvent(self,event):
        
        # when you want to destroy the dialog set this to True
        self._want_to_close = True
        self.ui.frmPassword.setVisible(True)
        
        if self.Password_Holder == 'qwe123':
            print '----- Closing UI -----'
            self.thread.stop()
        else:
            event.ignore()
            #self.setWindowState(QtCore.Qt.WindowMinimized)
        
       

    def CheckPass(self):
        self.Password_Holder = self.ui.lineEdit_Password.text()
        self.ui.lineEdit_Password.setText('')
        self.ui.frmPassword.setVisible(False)
        
  
    def AddTime(self):
    
        ##Adding values to alarm[] START and END of Shift
        StartShiftTime =["06:00 AM","06:36 AM","07:00 AM","06:00 PM","07:00 PM"]
        EndShiftTime =["03:36 PM","04:36 PM","05:36 PM","03:36 AM","04:36 AM","05:36 PM","06:36 PM"]
        self.thread.alarm = StartShiftTime + EndShiftTime
        
        Hourly_Chime =["08:00 AM","10:00 AM","12:00 PM","02:00 PM","04:00 PM","08:00 PM","10:00 PM","02:00 AM","04:00 AM"]
        ##Hourly_Chime2=["12:00 PM","01:00 PM","02:00 PM","03:00 PM","04:00 PM","05:00 PM","06:00 PM","09:00 PM","10:00 PM","11:00 PM"]
        ##Hourly_Chime2=["03:07 PM","03:09 PM"]
        self.thread.alarm_hourly = Hourly_Chime


        #Displaying text display all the time of alarm
        self.ui.text_display.append("Chime v 1.6.0")
        self.ui.text_display.append("Feb 23 2017, 03:29 PM")
        self.ui.text_display.append("Created by: Joeljie Taclendo [Wabbajak]")
        self.ui.text_display.append("-------------------------------------------------")
        self.ui.text_display.append("Start Shift Alarm:")
        self.ui.text_display.append(str(StartShiftTime))
        
        self.ui.text_display.append("-------------------------------------------------")
        self.ui.text_display.append("End Shift Alarm:")
        self.ui.text_display.append(str(EndShiftTime))
       
        self.ui.text_display.append("-------------------------------------------------")
        self.ui.text_display.append("Exercise Alarm below:")
        self.ui.text_display.append(str(self.thread.alarm_hourly))
          
        self.ui.text_display.append("-------------------------------------------------")   
        self.ui.text_display.moveCursor(QtGui.QTextCursor.End)
        
        #Start Thread
        self.thread.start()
        
        #Disable Start button
        #self.ui.btn_Start.setEnabled(False)   
       