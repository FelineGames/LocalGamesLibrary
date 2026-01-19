from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QLineEdit,
    QDialog, QTabWidget
)
from PySide6.QtCore import Qt

from backend.game_manager import load_library, save_library
from gui.add_game_dialog import AddGameDialog
from gui.game_card import GameCard


class SettingsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent_window = parent

        self.setWindowTitle("Settings")
        self.setFixedSize(400, 220)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)

        layout = QVBoxLayout(self)

        tabs = QTabWidget()
        layout.addWidget(tabs)

        # ✅ FIX: TAB STYLING HERE
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background: #171D25;
            }

            QTabBar::tab {
                background: #1F2F50;
                color: #aaaaaa;
                padding: 6px 14px;
                margin-right: 4px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }

            QTabBar::tab:selected {
                color: white;
                background: #2b406a;
                font-weight: bold;
            }

            QTabBar::tab:hover {
                color: white;
            }
        """)

        # ---------- General Tab ----------
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)

        label = QLabel("Main Header:")
        label.setStyleSheet("color:white;")

        self.headline_input = QLineEdit()
        self.headline_input.setText(parent.title_label.text())
        self.headline_input.setStyleSheet("""
            QLineEdit {
                background: #1F2F50;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 10px;
            }
        """)

        self.headline_input.textChanged.connect(self.update_live)

        general_layout.addWidget(label)
        general_layout.addWidget(self.headline_input)
        general_layout.addStretch()

        save_btn = QPushButton("Save Changes")
        save_btn.setFixedWidth(120)
        save_btn.setStyleSheet("""
            QPushButton {
                color: white;
                background: #1F2F50;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover { background: #2b406a; }
        """)
        save_btn.clicked.connect(self.accept)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        general_layout.addLayout(btn_layout)

        tabs.addTab(general_tab, "General")

        # ---------- Credits Tab ----------
        credits_tab = QWidget()
        credits_layout = QVBoxLayout(credits_tab)

        credits_label = QLabel(
            "A Trademark of FelineGamesStudio © Copyright 2023-2026\nDO NOT RE-DISTRUBUTE"
        )
        credits_label.setAlignment(Qt.AlignCenter)
        credits_label.setStyleSheet("color:white;font-size:13px;")

        credits_layout.addStretch()
        credits_layout.addWidget(credits_label)
        credits_layout.addStretch()

        tabs.addTab(credits_tab, "Credits")

        self.setStyleSheet("background:#171D25;")


    def update_live(self, text):
        self.parent_window.title_label.setText(text)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Local Games Library")
        self.resize(1920, 1080)

        self.games = load_library()

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        top_bar = QWidget()
        top_bar.setFixedHeight(55)
        top_bar.setStyleSheet("background:#171D25;")

        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(20, 0, 20, 0)

        # ---- Title ----
        self.title_label = QLabel("Library")
        self.title_label.setStyleSheet("color:white;font-size:20px;font-weight:bold;")

        # ---- Settings Button ----
        settings_btn = QPushButton("Settings")
        settings_btn.setStyleSheet("""
            QPushButton {
                color: #AAAAAA;
                background: transparent;
                font-size: 14px;
            }
            QPushButton:hover {
                color: white;
            }
        """)
        settings_btn.clicked.connect(self.open_settings)

        title_layout = QHBoxLayout()
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(settings_btn)
        title_layout.setSpacing(10)

        title_container = QWidget()
        title_container.setLayout(title_layout)

        # ---- Search ----
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search games...")
        self.search.setFixedHeight(32)
        self.search.setStyleSheet("""
            QLineEdit {
                background: #0E1621;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 10px;
            }
        """)
        self.search.textChanged.connect(self.apply_search)

        # ---- Add Button ----
        add_btn = QPushButton("+ Add Game")
        add_btn.setStyleSheet("""
            QPushButton {
                color: white;
                background: #1F2F50;
                padding: 6px 14px;
                border-radius: 4px;
            }
            QPushButton:hover { background: #2b406a; }
        """)
        add_btn.clicked.connect(self.add_game)

        top_layout.addWidget(title_container)
        top_layout.addStretch()
        top_layout.addWidget(self.search)
        top_layout.addWidget(add_btn)

        # ---- Library Area ----
        library_area = QWidget()
        library_area.setStyleSheet("background:#1F2F50;")

        self.library_layout = QVBoxLayout(library_area)
        self.library_layout.setAlignment(Qt.AlignTop)
        self.library_layout.setContentsMargins(20, 20, 20, 20)
        self.library_layout.setSpacing(15)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(library_area)
        scroll.setFrameShape(QScrollArea.NoFrame)

        scroll.setStyleSheet("""
            QScrollArea {
                background: #1F2F50;
                border: none;
            }
            QScrollArea > QWidget {
                background: #1F2F50;
            }
            QScrollArea > QWidget > QWidget {
                background: #1F2F50;
            }
        """)

        main_layout.addWidget(top_bar)
        main_layout.addWidget(scroll)

        self.refresh()

    def open_settings(self):
        dlg = SettingsDialog(self)
        dlg.exec()

    def refresh(self):
        while self.library_layout.count():
            item = self.library_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for game in self.games:
            card = GameCard(game, self)
            self.library_layout.addWidget(card)

    def add_game(self):
        dialog = AddGameDialog(self)
        if dialog.exec():
            self.games.append(dialog.game_data)
            save_library(self.games)
            self.refresh()

    def delete_game(self, game):
        self.games = [g for g in self.games if g != game]
        save_library(self.games)
        self.refresh()

    def apply_search(self, text):
        text = text.lower()

        while self.library_layout.count():
            item = self.library_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for game in self.games:
            if text in game["title"].lower() or text in game["author"].lower():
                card = GameCard(game, self)
                self.library_layout.addWidget(card)
