import sys
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
from screeninfo import get_monitors

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.browser = QtWebEngineWidgets.QWebEngineView()
        
        self.setCentralWidget(self.browser)
        global navtb
        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)
        self.combo = QComboBox()
        
        self.combo.insertItems(1,['Select Display'])
    
        for m in get_monitors():
            if m.is_primary == False:
                self.combo.insertItems(1,[m.name])

        home_btn = QAction("Home", self)
        reload_btn = QAction("Reload", self)
        back_btn = QAction("Back", self)
        next_btn = QAction("Forward", self)
        
        home_btn.setStatusTip("Go home")
        reload_btn.setStatusTip("Reload page")
        back_btn.setStatusTip("Back to previous page")
        next_btn.setStatusTip("Forward to next page")
        
        home_btn.triggered.connect(self.navigate_home)
        reload_btn.triggered.connect(self.browser.reload)
        back_btn.triggered.connect(self.browser.back)
        next_btn.triggered.connect(self.browser.forward)
        self.combo.currentIndexChanged.connect(self.ScreenSelection)

        navtb.addAction(home_btn)
        navtb.addAction(reload_btn)
        navtb.addAction(back_btn)
        navtb.addAction(next_btn)
        navtb.addWidget(self.combo)

        self.browser.load(QtCore.QUrl("https://app.antqueue.com/"))
        self.browser.settings().setAttribute(QWebEngineSettings.PlaybackRequiresUserGesture, False)
        global_settings = QtWebEngineWidgets.QWebEngineSettings.globalSettings()

        for attr in (
            QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled,
            QtWebEngineWidgets.QWebEngineSettings.FullScreenSupportEnabled,
            QtWebEngineWidgets.QWebEngineSettings.JavascriptEnabled,
            QtWebEngineWidgets.QWebEngineSettings.AutoLoadImages,
            QtWebEngineWidgets.QWebEngineSettings.LocalStorageEnabled,
        ):
            global_settings.setAttribute(attr, True)
        self.browser.page().fullScreenRequested.connect(self.FullscreenRequest)

    def ScreenSelection(self):
        global s
        s = app.screens()[self.combo.currentIndex()]

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://app.antqueue.com/"))
        
    @QtCore.pyqtSlot("QWebEngineFullScreenRequest")
    def FullscreenRequest(self, request,):
        request.accept()
        if request.toggleOn():
            navtb.setVisible(False)
            try:
                self.windowHandle().setScreen(s)
                self.showFullScreen()
            except NameError:
                QMessageBox.about(self, "Screen Manager", "A display is not selected yet!")
                navtb.setVisible(True)
        else:
            self.setCentralWidget(self.browser)
            self.browser.showNormal() 

if __name__ == "__main__":
    global app
    app = QtWidgets.QApplication(sys.argv) 
    w = MainWindow()
    app.setApplicationName("Screen Manager")
    app.setWindowIcon(QIcon('favicon.ico'))
    w.show()   
    sys.exit(app.exec_())