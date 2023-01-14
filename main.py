import sys,time

# import PyQt4 QtCore and QtGui modules
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from mainwindow import MainWindow
import get_screen




if __name__ == '__main__':

    # create application
    app = QApplication( sys.argv )
    
    # Create and display the splash screen
    splash_pix = QPixmap('splash_loading.png')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    app.processEvents()

    # Simulate something that takes time
    time.sleep(5)
    
    
    
    
    app.setApplicationName( 'My PyQt4 QtGui Project' )

    # create widsplashscreenget
    w = MainWindow()
    w.setWindowTitle( 'Set Chime Alarm' )
    s_width,s_height = get_screen.get_wh()
    
    w.setGeometry(s_width - 250,s_height - 350,241,300)
    
  

    w.show()
    
    
    
    #From Splashscreen code after splash call mainwindow
    splash.finish(w)
    
    
    
    
    # connection
    QObject.connect( app, SIGNAL( 'lastWindowClosed()' ), app, SLOT( 'quit()' ) )

    # execute application
    sys.exit( app.exec_() )
