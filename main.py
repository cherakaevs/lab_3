import datetime
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QFileDialog, QGridLayout
from PyQt5.QtGui import QFont

class DirectoryEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        callback(f"{datetime.datetime.now()}: {event.src_path} has been created")

    def on_deleted(self, event):
        callback(f"{datetime.datetime.now()}: {event.src_path} has been deleted")

    def on_modified(self, event):
        callback(f"{datetime.datetime.now()}: {event.src_path} has been modified")

    def on_moved(self, event):
        callback(f"{datetime.datetime.now()}: {event.src_path} moved to {event.dest_path}")

def stop_observer():
    global observer
    observer.stop()
    observer.join()

def start_observer(path):
    global observer, event_handler
    callback(f"{datetime.datetime.now()}: Started watching {path}")
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

def callback(message):
    global sctext_log
    sctext_log.append(message)
    return True

def exit():
    global app
    stop_observer()
    app.quit()

def choose_dir():
    global path
    dir_path = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
    if dir_path:
        start_observer(dir_path)

def save_txt():
    global sctext_log
    log = sctext_log.toPlainText()
    filePath, _ = QFileDialog.getSaveFileName(window, "Save log", "",
                                              "Text Files(*.txt) ")
    if filePath == "":
        return
    f = open(filePath, "w")
    f.write(log)

def clear_log():
    global sctext_log
    sctext_log.setText("")

if __name__ == "__main__":
    event_handler = DirectoryEventHandler()
    observer = Observer()
    path = None

    app = QApplication([])
    app.setStyle('Fusion')

    sctext_log = QTextEdit()
    sctext_log.setFont(QFont("Times New Roman", 12))
    sctext_log.setText(f"{datetime.datetime.now()}: application started")
    sctext_log.setReadOnly(True)

    button_choose_dir = QPushButton('Choose a folder')
    button_choose_dir.clicked.connect(choose_dir)
    button_choose_dir.setFixedSize(90, 20)
    button_exit = QPushButton('Exit')
    button_exit.clicked.connect(exit)
    button_exit.setFixedSize(90, 20)
    button_clear_textbox = QPushButton('Clear log')
    button_clear_textbox.clicked.connect(clear_log)
    button_clear_textbox.setFixedSize(90, 20)
    button_save_txt = QPushButton('Save txt')
    button_save_txt.clicked.connect(save_txt)
    button_save_txt.setFixedSize(90, 20)
    button_stop = QPushButton('Stop')
    button_stop.clicked.connect(observer.stop)
    button_stop.setFixedSize(90, 20)

    window = QWidget()
    window.setWindowTitle("Folder watcher")
    window.resize(640, 480)
    layout = QGridLayout()
    layout.addWidget(sctext_log, 0, 0, 1, 5)
    layout.addWidget(button_choose_dir, 1, 0)
    layout.addWidget(button_exit, 1, 5)
    layout.addWidget(button_clear_textbox, 1, 2)
    layout.addWidget(button_save_txt, 1, 3)
    layout.addWidget(button_stop, 1, 4)
    window.setLayout(layout)
    window.show()

    sys.exit(app.exec_())


