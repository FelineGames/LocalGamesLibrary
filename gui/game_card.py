import os
import sys
import subprocess
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class GameCard(QWidget):
    def __init__(self, game, main_window):
        super().__init__()

        self.game = game
        self.main_window = main_window

        self.setStyleSheet("""
            QWidget {
                background: transparent;
                border-radius:6px;
            }
        """)
        self.setFixedHeight(90)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        icon = QLabel()
        icon.setFixedSize(64, 64)
        icon.setStyleSheet("background:black;")
        if game.get("icon") and os.path.exists(game["icon"]):
            pix = QPixmap(game["icon"]).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon.setPixmap(pix)

        text_layout = QVBoxLayout()
        title = QLabel(game["title"])
        title.setStyleSheet("color:white;font-size:16px;font-weight:bold;")
        author = QLabel(game["author"])
        author.setStyleSheet("color:#bbbbbb;font-size:12px;")

        text_layout.addWidget(title)
        text_layout.addWidget(author)
        text_layout.addStretch()

        btn_layout = QHBoxLayout()

        play = QPushButton()
        play.setIcon(QIcon(resource_path("assets/play.png")))
        play.clicked.connect(self.play_game)

        edit = QPushButton()
        edit.setIcon(QIcon(resource_path("assets/edit.png")))
        edit.clicked.connect(self.edit_library)

        folder = QPushButton()
        folder.setIcon(QIcon(resource_path("assets/folder_icon.png")))
        folder.clicked.connect(self.open_folder)

        delete = QPushButton()
        delete.setIcon(QIcon(resource_path("assets/trash.png")))
        delete.clicked.connect(self.delete_game)

        for b in (play, edit, folder, delete):
            b.setFixedSize(36, 36)
            b.setStyleSheet("background:#000000;")

        btn_layout.addWidget(play)
        btn_layout.addWidget(edit)
        btn_layout.addWidget(folder)
        btn_layout.addWidget(delete)

        layout.addWidget(icon)
        layout.addLayout(text_layout)
        layout.addStretch()
        layout.addLayout(btn_layout)

    def play_game(self):
        subprocess.Popen(self.game["exe"], shell=True)

    def open_folder(self):
        folder = os.path.dirname(self.game["exe"])
        os.startfile(folder)

    def edit_library(self):
        base = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.path.abspath(".")
        path = os.path.join(base, "library.json")
        if os.path.exists(path):
            os.startfile(path)
        else:
            QMessageBox.warning(self, "Error", "library.json not found")

    def delete_game(self):
        self.setParent(None)
        if self.game in self.main_window.games:
            self.main_window.games.remove(self.game)
