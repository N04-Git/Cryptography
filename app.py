import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton
)
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("File Transfer")
        self.setGeometry(400, 400, 1000, 750)
        
        self.connectionBoxes = []
        
        self.init_ui()

    def init_ui(self):
        # Widgets
        centralWidget = QWidget()
        centralWidget.setStyleSheet("border: 1px solid #FF2FCC")
        self.setCentralWidget(centralWidget)
        
        vbox = QVBoxLayout()
        centralWidget.setLayout(vbox)

        
            # Top
        topFrame = QFrame()
        topFrame.setStyleSheet("""
                               max-height: 230px;
                               """)
        topFrame.setLayout(QHBoxLayout())
        vbox.addWidget(topFrame)

        self.topLeftFrame = QFrame()
        self.topLeftFrame.setLayout(QHBoxLayout())
        self.topLeftFrame.layout().setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.topLeftFrame.setStyleSheet("""
                                        max-width: 750px
                                        """)


        self.topRightFrame = QFrame()
        self.topRightFrame.setLayout(QGridLayout())
        self.topRightFrame.setStyleSheet("""
                                        max-width: 200px
                                        """)

        topFrame.layout().addWidget(self.topLeftFrame)
        topFrame.layout().addWidget(self.topRightFrame)

                # TOP LEFT


                # TOP RIGHT
        custom_client_label = QLabel("Manuel Client Info")
        custom_client_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)


        host_label = QLabel("Custom IP")
        host_label.setStyleSheet("""
                                max-width: 100px;
                                """)
        host_line = QLineEdit()
        host_line.setStyleSheet("""
                                max-width: 100px;
                                """)    
        port_label = QLabel("Custom PORT")
        port_label.setStyleSheet("""
                                max-width: 100px;
                                """)
        port_line = QLineEdit()
        port_line.setStyleSheet("""
                                max-width: 100px;
                                """)
        connect_btn = QPushButton("CONNECT")

        server_info_label = QLabel("Server Info")
        server_info_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        shost_label = QLabel("HOST")
        shost_line = QLineEdit()
        sport_label = QLabel("PORT")
        sport_line = QLineEdit()
        slisten_btn = QPushButton("START SERVER")

        self.topRightFrame.layout().addWidget(custom_client_label, 0, 0, 1, 0)
        self.topRightFrame.layout().addWidget(host_label, 1, 0)
        self.topRightFrame.layout().addWidget(host_line, 1, 1)
        self.topRightFrame.layout().addWidget(port_label, 2, 0)
        self.topRightFrame.layout().addWidget(port_line, 2, 1)
        self.topRightFrame.layout().addWidget(connect_btn, 3, 0, 1, 0)
        
        self.topRightFrame.layout().addWidget(server_info_label, 4, 0, 1, 0)
        self.topRightFrame.layout().addWidget(shost_label, 5, 0)
        self.topRightFrame.layout().addWidget(shost_line, 5, 1)
        self.topRightFrame.layout().addWidget(sport_label, 6, 0)
        self.topRightFrame.layout().addWidget(sport_line, 6, 1)
        self.topRightFrame.layout().addWidget(slisten_btn, 7, 0, 1, 0)

            # Bottom
        bottomFrame = QFrame()
        bottomFrame.setLayout(QHBoxLayout())
        vbox.addWidget(bottomFrame)

        self.bottomLeftFrame = QFrame()
        self.bottomLeftFrame.setLayout(QGridLayout())

        self.bottomRightFrame = QFrame()
        self.bottomRightFrame.setLayout(QVBoxLayout())

        bottomFrame.layout().addWidget(self.bottomLeftFrame)
        bottomFrame.layout().addWidget(self.bottomRightFrame)

                # BOTTOM LEFT


                # BOTTOM RIGHT
        connection_state = QLabel("CONNECTED : NO")
        self.bottomRightFrame.layout().addWidget(connection_state)




    def addConnectionBox(self, info):
        """
        info : list 
        [0] - name (string)
        [1] - ip/port (tuple)
        """
        # Create widget
        frame = QFrame()
        frame.setStyleSheet("""
                            max-width: 120px;
                            """)
        self.topLeftFrame.layout().addWidget(frame)
        frame.setLayout(QVBoxLayout())
        frame.layout().setContentsMargins(5, 0, 5, 0)

        # Add infos to frame
        boxLabel = QLabel(info[0])
        ipLabel = QLabel(f" IP : {info[1][0]}")
        portLabel = QLabel(f" IP : {info[1][1]}")
        
        frame.layout().addWidget(boxLabel)
        frame.layout().addWidget(ipLabel)
        frame.layout().addWidget(portLabel)

if __name__ == '__main__':
    # CREATE EVENTS HANDLER
    app = QApplication(sys.argv)

    # CREATE MAIN-WINDOW
    mainWindow = MainWindow()
    mainWindow.show()

    # RUN PyQT System handler
    app.exec()