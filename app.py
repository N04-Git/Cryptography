import network, integrity, conversion
import sys
import os
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
    QPushButton,
    QCheckBox,
    QMessageBox,
    QFileDialog,
    QComboBox
)
from PyQt6.QtCore import Qt


# Clean terminal
os.system('cls')

class InfoDialog(QMessageBox):
    def __init__(self, title, msg):
        super().__init__()
        
        self.setWindowTitle(title)
        self.setText(msg)
        
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        self.exec()

class FileDialog(QFileDialog):
    def __init__(self):
        super().__init__()
        
        # Open dialog
        self.selected = self.getOpenFileName(self)
        self.fpath = self.selected[0]
        self.ftype = self.selected[1]
        

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Secure File Transfer")
        self.setGeometry(400, 400, 1000, 750)
        
        # File Path to send
        self.filePath = ''
        
        # Display
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
        self.host_line = QLineEdit()
        self.host_line.setStyleSheet("""
                                max-width: 100px;
                                """)    
        port_label = QLabel("Custom PORT")
        port_label.setStyleSheet("""
                                max-width: 100px;
                                """)
        self.port_line = QLineEdit()
        self.port_line.setStyleSheet("""
                                max-width: 100px;
                                """)
        connect_btn = QPushButton("CONNECTION")
        connect_btn.clicked.connect(self.connectButtonClicked)

        server_info_label = QLabel("SERVEUR")
        server_info_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        shost_label = QLabel("HOST")
        self.shost_line = QLineEdit()
        sport_label = QLabel("PORT")
        self.sport_line = QLineEdit()
        slisten_btn = QPushButton("DEMARRER")
        slisten_btn.clicked.connect(self.listenButtonClicked)

        # TMP PRESET VALUES
        self.host_line.setText('127.0.0.1')
        self.port_line.setText('8080')
        self.shost_line.setText('127.0.0.1')
        self.sport_line.setText('8080')
        # TMP PRESET VALUES
        

        self.topRightFrame.layout().addWidget(custom_client_label, 0, 0, 1, 0)
        self.topRightFrame.layout().addWidget(host_label, 1, 0)
        self.topRightFrame.layout().addWidget(self.host_line, 1, 1)
        self.topRightFrame.layout().addWidget(port_label, 2, 0)
        self.topRightFrame.layout().addWidget(self.port_line, 2, 1)
        self.topRightFrame.layout().addWidget(connect_btn, 3, 0, 1, 0)
        
        self.topRightFrame.layout().addWidget(server_info_label, 4, 0, 1, 0)
        self.topRightFrame.layout().addWidget(shost_label, 5, 0)
        self.topRightFrame.layout().addWidget(self.shost_line, 5, 1)
        self.topRightFrame.layout().addWidget(sport_label, 6, 0)
        self.topRightFrame.layout().addWidget(self.sport_line, 6, 1)
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
        import_btn = QPushButton("Importer")
        self.filename_label = QLabel("Fichier : ")
        self.filepath_label = QLabel("Emplacement : ")
        self.filehash_label = QLabel("Sha-256 :")
        encryption_box = QCheckBox("Chiffrer")
        encryptions_options = QComboBox()
        encryptions_options.addItems(['AES', 'DES', 'BLOWFISH', 'RSA', 'ECC'])
        send_btn = QPushButton("Envoyer")

        import_btn.clicked.connect(self.importButtonClicked)
        send_btn.clicked.connect(self.sendButtonClicked)

        self.bottomLeftFrame.layout().addWidget(import_btn, 0, 0, 1, 2)
        self.bottomLeftFrame.layout().addWidget(self.filename_label, 1, 0)
        self.bottomLeftFrame.layout().addWidget(self.filepath_label, 1, 1)
        self.bottomLeftFrame.layout().addWidget(self.filehash_label, 2, 0, 1, 2)
        self.bottomLeftFrame.layout().addWidget(encryption_box, 3, 0)
        self.bottomLeftFrame.layout().addWidget(encryptions_options, 3, 1)
        self.bottomLeftFrame.layout().addWidget(send_btn, 4, 0, 1, 2)

                # BOTTOM RIGHT
        
        self.connection_ping = QLabel("PING :")
        self.connection_ip = QLabel("IP :")
        self.connection_port = QLabel("PORT :")
        self.connection_packetsCounter = QLabel("PAQUETS TRANSMIS : ")
        self.connection_emptyPacketsCounter = QLabel('PAQUETS VIDES : ')
        
        self.connection_refresh = QPushButton("REFRESH")
        self.connection_refresh.clicked.connect(self.refreshButtonClicked)

        self.bottomRightFrame.layout().addWidget(self.connection_ping)
        self.bottomRightFrame.layout().addWidget(self.connection_ip)
        self.bottomRightFrame.layout().addWidget(self.connection_port)
        self.bottomRightFrame.layout().addWidget(self.connection_packetsCounter)
        self.bottomRightFrame.layout().addWidget(self.connection_emptyPacketsCounter)

        self.bottomRightFrame.layout().addWidget(self.connection_refresh)

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

    def listenButtonClicked(self):
        # Get field values
        host = self.shost_line.text()
        port = self.sport_line.text()
        
        # Create server
        s = network.Server(host, int(port))
        s.main_signal.connect(self.newClientCreated)
        
    def connectButtonClicked(self):
        # Get field values
        host = self.host_line.text()
        port = self.port_line.text()

        # Create client
        instance = network.Client(host, int(port))
        
        # Check if client is in the Client list
        if not instance in network.Client.instances:
            # Failed to connect
            InfoDialog('Connexion au client', 'Impossible de se connecter.')
            return
        
        self.newClientCreated(instance)

    def refreshButtonClicked(self):
        if len(network.Connection.instances) > 0:
            # Get last connection instance
            obj = network.Connection.instances[-1]
            obj.refreshConnection()
            
        else:
            print('No Active connection :', network.Connection.instances)

    def newClientCreated(self, instance:network.Connection):
        print('[+] New client created :', instance)
        
        # Connect client's signals
        instance.ping_updated.connect(self.updatePingLabel)
        instance.emptyPackets_updated.connect(self.updateEmptyPacketsCounterLabel)
        instance.packetsCounter_updated.connect(self.updatePacketsCounterLabel)
        
        # Refresh connnection to display ping
        instance.refreshConnection()

    def updatePingLabel(self, ping:float):
        # Update label value
        self.connection_ping.setText(f'PING : {str(ping)[:5]}')
        
    def updateEmptyPacketsCounterLabel(self, emptyPackets:int):
        # Update label value
        self.connection_emptyPacketsCounter.setText(f"EMPTY PACKETS : {emptyPackets}")
    
    def updatePacketsCounterLabel(self, packets:int):
        # Update label value
        self.connection_packetsCounter.setText(f"PACKETS : {packets}")

    def importButtonClicked(self):
        # Prompt which file location
        dialog = FileDialog()
        
        # Save file path
        self.filePath = dialog.fpath

        # Get info
        file_info = integrity.getFileInfo(self.filePath)
        
        # Update widgets info
        self.filename_label.setText("Fichier : " + file_info[0] + ' - ' + str(file_info[2]) + ' octets')
        
        self.filepath_label.setText("Emplacement : " + file_info[1])
        
        self.filehash_label.setText("Sha-256 : " + file_info[3])

    def sendButtonClicked(self):
        # Get file data
        with open(self.filePath, 'rb') as f:
            fdata = f.read()
        
        # Encrypt file if needed
        # ...
        # ...
        
        # Send file bytes
        network.Connection.instances[-1].sendFile(file_bytes=fdata, filename=integrity.getFileInfo(self.filePath)[0])


if __name__ == '__main__':
    # CREATE EVENTS HANDLER
    app = QApplication(sys.argv)

    # CREATE MAIN-WINDOW
    mainWindow = MainWindow()
    mainWindow.show()

    # RUN PyQT System handler
    app.exec()