import os
import sys
import subprocess

from PySide6.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QSize


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class GameCard(QWidget):
    def __init__(self, game, main_window):
        super().__init__()

        self.game = game
        self.main_window = main_window

        self.setStyleSheet("""
            QWidget {
                background: transparent;
                border-radius: 6px;
            }
        """)
        self.setFixedHeight(90)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        icon = QLabel()
        icon.setFixedSize(64, 64)
        icon.setStyleSheet("background:black; border-radius:6px;")

        if game.get("icon") and os.path.exists(game["icon"]):
            pix = QPixmap(game["icon"]).scaled(
                64, 64,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
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
        btn_layout.setSpacing(8)

        play_btn = QPushButton()
        play_btn.setIcon(QIcon(resource_path("assets/play.png")))
        play_btn.setIconSize(QSize(22, 22))
        play_btn.clicked.connect(self.play_game)

        folder_btn = QPushButton()
        folder_btn.setIcon(QIcon(resource_path("assets/folder_icon.png")))
        folder_btn.setIconSize(QSize(22, 22))
        folder_btn.clicked.connect(self.open_folder)

        delete_btn = QPushButton()
        delete_btn.setIcon(QIcon(resource_path("assets/trash.png")))
        delete_btn.setIconSize(QSize(22, 22))
        delete_btn.clicked.connect(self.delete_game)

        for b in (play_btn, folder_btn, delete_btn):
            b.setFixedSize(36, 36)
            b.setCursor(Qt.PointingHandCursor)
            b.setStyleSheet("""
                QPushButton {
                    background: #000000;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background: #222222;
                }
                QPushButton:pressed {
                    background: #111111;
                }
            """)

        btn_layout.addWidget(play_btn)
        btn_layout.addWidget(folder_btn)
        btn_layout.addWidget(delete_btn)

        layout.addWidget(icon)
        layout.addLayout(text_layout)
        layout.addStretch()
        layout.addLayout(btn_layout)

    def play_game(self):
        subprocess.Popen(self.game["exe"], shell=True)

    def open_folder(self):
        folder = os.path.dirname(self.game["exe"])
        os.startfile(folder)

    def delete_game(self):
        self.main_window.delete_game(self.game)
