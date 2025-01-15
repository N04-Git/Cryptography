import network, integrity, conversion
import sys
import os
import threading
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
    def __init__(self, title, msg, type=0):
        super().__init__()
        
        self.setWindowTitle(title)
        self.setText(msg)

        if type != 0:
            if type == 1:
                buttons = {
                    "Oui": QMessageBox.ButtonRole.YesRole,
                    "Non": QMessageBox.ButtonRole.NoRole
                }
            
            # Add buttons
            for btn_txt, btn_role in buttons.items():
                button = self.addButton(btn_txt, btn_role)

        self.exec()
    
    def get_clicked_button(self):
        return self.clickedButton().text()

class FileDialog(QFileDialog):
    def __init__(self, onlyPath=False):
        super().__init__()

        if onlyPath:
            # Open directory dialog
            self.fpath = self.getExistingDirectory(self, 'Choisir le dossier')
        else:
            # Open file dialog
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
        self.setCentralWidget(centralWidget)
        
        vbox = QVBoxLayout()
        centralWidget.setLayout(vbox)
        
        centralWidget.setStyleSheet("""
            QPushButton {
                background-color: #796394;
            }
            QPushButton:hover {
                background-color: #9f88bb;
            }
            
            """)
        
            # Top
        topFrame = QFrame()
        topFrame.setObjectName('topFrame')
        topFrame.setStyleSheet(""" QWidget#topFrame {
            max-height: 230px;
            border: 1px solid #FFFFFF !important;
            border-radius: 5px;
        }""")
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
        self.topRightFrame.setObjectName('topRightFrame')
        self.topRightFrame.setStyleSheet(""" QWidget#topRightFrame {
            max-width: 200px;
            border: 1px solid #626274; 
        }""")

        topFrame.layout().addWidget(self.topLeftFrame)
        topFrame.layout().addWidget(self.topRightFrame)

                # TOP LEFT
        scan_frame = QFrame()
        scan_frame.setObjectName('scanFrame')
        scan_frame.setStyleSheet(""" QWidget#scanFrame {
            max-width: 100px;
            border: 1px solid #626274;
        }""")
        scan_frame.setLayout(QGridLayout())
        scan_port_label = QLabel("Port")
        self.scan_port_line = QLineEdit()
        scan_button = QPushButton("SCAN")
        scan_button.clicked.connect(self.scanButtonClicked)
        
        self.scan_port_line.setText('1122')
        self.topLeftFrame.layout().addWidget(scan_frame)
        scan_frame.layout().addWidget(scan_port_label, 0, 0)
        scan_frame.layout().addWidget(self.scan_port_line, 1, 0)
        scan_frame.layout().addWidget(scan_button, 2, 0)

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
        connect_btn = QPushButton("CONNEXION")
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
        self.port_line.setText('1122')
        self.shost_line.setText('0.0.0.0')
        self.sport_line.setText('1122')
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
        self.bottomLeftFrame.setObjectName('bottomLeftframe')
        self.bottomLeftFrame.setStyleSheet(""" QWidget#bottomLeftframe {
            border: 1px solid #FFFFFF;
            border-radius: 5px;
            margin-right: 5px;
        }""")
        self.bottomLeftFrame.setLayout(QGridLayout())

        self.bottomRightFrame = QFrame()
        self.bottomRightFrame.setObjectName('bottomRightFrame')
        self.bottomRightFrame.setStyleSheet(""" QWidget#bottomRightFrame {
            border: 1px solid #FFFFFF;
            border-radius: 5px;
            margin-left: 5px;
        }""")
        self.bottomRightFrame.setLayout(QVBoxLayout())

        bottomFrame.layout().addWidget(self.bottomLeftFrame)
        bottomFrame.layout().addWidget(self.bottomRightFrame)

                # BOTTOM LEFT
        import_btn = QPushButton("Importer")
        self.filename_label = QLabel("Fichier : ")
        self.filepath_label = QLabel("Emplacement : ")
        self.filehash_label = QLabel("Sha-256 :")
        self.encryption_box = QCheckBox("Chiffrer")
        self.encryptions_options = QComboBox()
        self.encryptions_options.addItems(conversion.encryptions)
        send_btn = QPushButton("Envoyer")

        import_btn.clicked.connect(self.importButtonClicked)
        send_btn.clicked.connect(self.sendButtonClicked)

        self.bottomLeftFrame.layout().addWidget(import_btn, 0, 0, 1, 2)
        self.bottomLeftFrame.layout().addWidget(self.filename_label, 1, 0)
        self.bottomLeftFrame.layout().addWidget(self.filepath_label, 1, 1)
        self.bottomLeftFrame.layout().addWidget(self.filehash_label, 2, 0, 1, 2)
        self.bottomLeftFrame.layout().addWidget(self.encryption_box, 3, 0)
        self.bottomLeftFrame.layout().addWidget(self.encryptions_options, 3, 1)
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
        
        # Add new frame to topLeftFrame
        self.topLeftFrame.layout().addWidget(frame)
        
        # Setup layout
        frame.setLayout(QVBoxLayout())
        frame.layout().setContentsMargins(5, 0, 5, 0)

        # Add infos to frame
        boxLabel = QLabel(info[0])
        ipLabel = QLabel(f"IP : {info[1][0]}")
        portLabel = QLabel(f"Port : {info[1][1]}")
        connectBtn = QPushButton("CONNEXION")
        connectBtn.clicked.connect(lambda: self.connectButtonClicked(custom=(info[1][0], info[1][1])))
        frame.layout().addWidget(boxLabel)
        frame.layout().addWidget(ipLabel)
        frame.layout().addWidget(portLabel)
        frame.layout().addWidget(connectBtn)

    def listenButtonClicked(self):
        # Get field values
        host = self.shost_line.text()
        port = self.sport_line.text()
        
        # Create server
        s = network.Server(host, int(port))
        s.main_signal.connect(self.newClientCreated)
        
    def connectButtonClicked(self, custom=None):
        if custom:
            host = custom[0]
            port = custom[1]
        else:
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
        instance.address_updated.connect(self.updateAddressLabel)
        instance.file_sent.connect(self.fileSent)
        instance.file_received.connect(self.fileReceived)
        instance.connection_closed.connect(self.clientDisconnected)
        
        # Refresh connnection to display ping
        instance.refreshConnection()

        # Info
        InfoDialog("Connexion", f"Nouvelle connexion !")

    def updateAddressLabel(self, address):
        ip, port = address
        self.connection_ip.setText(f"IP : {ip}")
        self.connection_port.setText(f"PORT : {str(port)}")

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
        # Check if file was selected
        # Save file path
        self.filePath = dialog.fpath

        # Get info
        if not self.filePath:
            return
        
        file_info = integrity.getFileInfo(self.filePath)
        
        # Update widgets info
        self.filename_label.setText("Fichier : " + file_info[0] + ' - ' + str(file_info[2]) + ' octets')
        
        self.filepath_label.setText("Emplacement : " + file_info[1])
        
        self.filehash_label.setText("Sha-256 : " + file_info[3])

    def sendButtonClicked(self):
        # Check if any file selected
        if not self.filePath:
            return
        
        # Get file data
        with open(self.filePath, 'rb') as f:
            fdata = f.read()
        
        # Default values
        index = None
        k = None
        
        # Encrypt file if needed
        if self.encryption_box.isChecked():
            
            # Send public key request
            network.Connection.instances[-1].askPublicKey()
            
            # Wait for public key
            while not network.Connection.instances[-1].public_key:        
                continue
        
            # Check selected encryption
            index = self.encryptions_options.currentIndex()
            
            # Encrypt file
            fdata, key = conversion.encryptFile(fdata, index)
        
            # encrypt key with client's public key
            if key:    
                k = network.RSAC.encrypt(data=key, public_key=network.Connection.instances[-1].public_key)
        
        # Send file bytes & encrypted key & chosen index
        network.Connection.instances[-1].sendFile(file_bytes=fdata, filename=integrity.getFileInfo(self.filePath)[0], key=k, enc_index=index)

    def scanButtonClicked(self):
        # Get target port
        p = int(self.scan_port_line.text())
        
        # Start scan
        analyzer = network.Analyzer()
        analyzer.serverDetected.connect(self.addConnectionBox)
        
        t = threading.Thread(target=analyzer.scanNetwork, args=[p,])
        t.daemon = True
        t.start()
        InfoDialog('Scan', "Recherche d'un server...")
        
    def fileSent(self):
        # file sent
        dialog = InfoDialog('INFO', 'Fichier envoyé !')
        
    def fileReceived(self, fileInfo:tuple):
        fname, fsize, fbytes = fileInfo
        
        # file received
        dialog = InfoDialog('INFO', f'Fichier reçu :\n- {fname}\n- {str(fsize/10000)[:7]}Mo\n\n\tEnregistré ?', 1)
        if dialog.get_clicked_button() == 'Oui':
            # Save file
            # Get filedialog
            fdg = FileDialog(True)
            if fdg.fpath:
                # Save file
                with open(fdg.fpath+'\\'+fname, 'wb') as newFile:
                    newFile.write(fbytes)
                InfoDialog('Succès', f'Fichier enregistré !\n>> {fdg.fpath+fname}')

    def clientDisconnected(self, errorMsg):
        # Show info dialog
        dg = InfoDialog("Connexion", f"Le client s'est déconnecté.\n<<{errorMsg}>>\nFermeture de la connexion...")

if __name__ == '__main__':
    # CREATE EVENTS HANDLER
    app = QApplication(sys.argv)

    # CREATE MAIN-WINDOW
    mainWindow = MainWindow()
    mainWindow.show()
    
    # RUN PyQT System handler
    app.exec()