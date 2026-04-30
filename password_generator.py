import sys
import random
import string
import pyperclip
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTabWidget, QLabel, QLineEdit, 
                             QPushButton, QSlider, QCheckBox, QGroupBox)
from PyQt6.QtCore import Qt, QTimer

class PasswordGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password generator")
        self.setFixedSize(500, 650)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        
        # Tabs
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)
        
        self.tab_password = QWidget()
        self.tab_passphrase = QWidget()
        
        self.tabs.addTab(self.tab_password, "Password")
        self.tabs.addTab(self.tab_passphrase, "Passphrase")
        
        self.setup_password_tab()
        self.setup_passphrase_tab()
        self.apply_styles()
        
        self.generate_password()
        
    def setup_password_tab(self):
        layout = QVBoxLayout(self.tab_password)
        
        # Result area
        result_layout = QHBoxLayout()
        self.result_entry = QLineEdit()
        self.result_entry.setReadOnly(True)
        self.result_entry.setMinimumHeight(40)
        font = self.result_entry.font()
        font.setPointSize(16)
        font.setFamily("Courier")
        self.result_entry.setFont(font)
        result_layout.addWidget(self.result_entry)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setMinimumHeight(40)
        self.refresh_btn.clicked.connect(self.generate_password)
        result_layout.addWidget(self.refresh_btn)
        
        self.copy_btn = QPushButton("Copy")
        self.copy_btn.setMinimumHeight(40)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        result_layout.addWidget(self.copy_btn)
        
        layout.addLayout(result_layout)
        
        # Options Group
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout(options_group)
        layout.addWidget(options_group)
        
        # Length
        self.length_label = QLabel("Length: 14")
        options_layout.addWidget(self.length_label)
        self.length_slider = QSlider(Qt.Orientation.Horizontal)
        self.length_slider.setRange(5, 128)
        self.length_slider.setValue(14)
        self.length_slider.valueChanged.connect(self.update_length)
        options_layout.addWidget(self.length_slider)
        
        # Include Checkboxes
        options_layout.addWidget(QLabel("Include"))
        checkbox_layout = QHBoxLayout()
        self.cb_upper = QCheckBox("A-Z")
        self.cb_upper.setChecked(True)
        self.cb_lower = QCheckBox("a-z")
        self.cb_lower.setChecked(True)
        self.cb_nums = QCheckBox("0-9")
        self.cb_nums.setChecked(True)
        self.cb_syms = QCheckBox("!@#$%^&*")
        self.cb_syms.setChecked(False)
        
        for cb in [self.cb_upper, self.cb_lower, self.cb_nums, self.cb_syms]:
            cb.stateChanged.connect(self.generate_password)
            checkbox_layout.addWidget(cb)
        options_layout.addLayout(checkbox_layout)
        
        # Minimums
        mins_layout = QHBoxLayout()
        mins_layout.addWidget(QLabel("Minimum numbers:"))
        self.min_nums_entry = QLineEdit("1")
        self.min_nums_entry.textChanged.connect(self.generate_password)
        mins_layout.addWidget(self.min_nums_entry)
        
        mins_layout.addWidget(QLabel("Minimum special:"))
        self.min_spec_entry = QLineEdit("0")
        self.min_spec_entry.textChanged.connect(self.generate_password)
        mins_layout.addWidget(self.min_spec_entry)
        options_layout.addLayout(mins_layout)
        
        # Ambiguous
        self.cb_ambiguous = QCheckBox("Avoid ambiguous characters (l, 1, I, O, 0)")
        self.cb_ambiguous.stateChanged.connect(self.generate_password)
        options_layout.addWidget(self.cb_ambiguous)
        
        layout.addStretch()

    def setup_passphrase_tab(self):
        layout = QVBoxLayout(self.tab_passphrase)
        
        # Result area
        result_layout = QHBoxLayout()
        self.pp_result_entry = QLineEdit()
        self.pp_result_entry.setReadOnly(True)
        self.pp_result_entry.setMinimumHeight(40)
        font = self.pp_result_entry.font()
        font.setPointSize(16)
        font.setFamily("Courier")
        self.pp_result_entry.setFont(font)
        result_layout.addWidget(self.pp_result_entry)
        
        self.pp_refresh_btn = QPushButton("Refresh")
        self.pp_refresh_btn.setMinimumHeight(40)
        self.pp_refresh_btn.clicked.connect(self.generate_passphrase)
        result_layout.addWidget(self.pp_refresh_btn)
        
        self.pp_copy_btn = QPushButton("Copy")
        self.pp_copy_btn.setMinimumHeight(40)
        self.pp_copy_btn.clicked.connect(self.copy_pp_to_clipboard)
        result_layout.addWidget(self.pp_copy_btn)
        
        layout.addLayout(result_layout)
        
        # Options
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout(options_group)
        layout.addWidget(options_group)
        
        self.pp_words_label = QLabel("Number of words: 4")
        options_layout.addWidget(self.pp_words_label)
        self.pp_words_slider = QSlider(Qt.Orientation.Horizontal)
        self.pp_words_slider.setRange(3, 12)
        self.pp_words_slider.setValue(4)
        self.pp_words_slider.valueChanged.connect(self.update_pp_words)
        options_layout.addWidget(self.pp_words_slider)
        
        sep_layout = QHBoxLayout()
        sep_layout.addWidget(QLabel("Separator:"))
        self.pp_sep_entry = QLineEdit("-")
        self.pp_sep_entry.textChanged.connect(self.generate_passphrase)
        sep_layout.addWidget(self.pp_sep_entry)
        options_layout.addLayout(sep_layout)
        
        self.pp_cap_cb = QCheckBox("Capitalize words")
        self.pp_cap_cb.stateChanged.connect(self.generate_passphrase)
        options_layout.addWidget(self.pp_cap_cb)
        
        layout.addStretch()

        self.wordlist = [
            "apple", "brave", "crane", "dance", "eagle", "flame", "grape", "house", "image", "juice",
            "knife", "lemon", "mouse", "night", "ocean", "peace", "queen", "river", "snake", "train",
            "uncle", "voice", "water", "x-ray", "yacht", "zebra", "cloud", "storm", "light", "shadow",
            "forest", "mountain", "valley", "spring", "summer", "autumn", "winter", "silver", "gold"
        ]
        self.generate_passphrase()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                font-size: 14px;
            }
            QLineEdit {
                border: 1px solid #dcdcdc;
                border-radius: 6px;
                padding: 5px 10px;
                background-color: white;
            }
            QLineEdit:read-only {
                background-color: #fcfcfc;
            }
            QPushButton {
                background-color: #0d6efd;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                padding: 6px 15px;
                border: none;
            }
            QPushButton:hover {
                background-color: #0b5ed7;
            }
            QPushButton:pressed {
                background-color: #0a58ca;
            }
            QGroupBox {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 20px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
                font-weight: 600;
                color: #333;
            }
            QTabWidget::pane {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background: #f8f9fa;
            }
            QTabBar::tab {
                background: #e9ecef;
                color: #495057;
                border: 1px solid #dee2e6;
                padding: 10px 25px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #f8f9fa;
                color: #0d6efd;
                font-weight: bold;
                border-bottom-color: #f8f9fa;
            }
            QMainWindow {
                background-color: #f0f2f5;
            }
        """)

    def update_length(self, value):
        self.length_label.setText(f"Length: {value}")
        self.generate_password()
        
    def update_pp_words(self, value):
        self.pp_words_label.setText(f"Number of words: {value}")
        self.generate_passphrase()

    def generate_password(self):
        try:
            length = self.length_slider.value()
            
            use_upper = self.cb_upper.isChecked()
            use_lower = self.cb_lower.isChecked()
            use_nums = self.cb_nums.isChecked()
            use_syms = self.cb_syms.isChecked()
            avoid_ambig = self.cb_ambiguous.isChecked()
            
            try:
                min_nums = int(self.min_nums_entry.text() or "0")
            except ValueError:
                min_nums = 0
                
            try:
                min_spec = int(self.min_spec_entry.text() or "0")
            except ValueError:
                min_spec = 0

            upper_chars = string.ascii_uppercase
            lower_chars = string.ascii_lowercase
            num_chars = string.digits
            sym_chars = "!@#$%^&*"
            ambiguous_chars = "l1IO0"

            if avoid_ambig:
                upper_chars = "".join([c for c in upper_chars if c not in ambiguous_chars])
                lower_chars = "".join([c for c in lower_chars if c not in ambiguous_chars])
                num_chars = "".join([c for c in num_chars if c not in ambiguous_chars])

            pool = ""
            if use_upper: pool += upper_chars
            if use_lower: pool += lower_chars
            if use_nums: pool += num_chars
            if use_syms: pool += sym_chars

            if not pool:
                self.result_entry.setText("Select at least one character set.")
                return

            password_chars = []
            
            if use_nums and min_nums > 0:
                for _ in range(min(min_nums, length)):
                    password_chars.append(random.choice(num_chars))
                    
            if use_syms and min_spec > 0:
                for _ in range(min(min_spec, length - len(password_chars))):
                    password_chars.append(random.choice(sym_chars))

            remaining_length = length - len(password_chars)
            for _ in range(remaining_length):
                password_chars.append(random.choice(pool))

            random.shuffle(password_chars)
            password = "".join(password_chars)[:length]
            
            self.result_entry.setText(password)
        except Exception:
            pass

    def generate_passphrase(self):
        try:
            num_words = self.pp_words_slider.value()
            separator = self.pp_sep_entry.text()
            capitalize = self.pp_cap_cb.isChecked()

            words = []
            for _ in range(num_words):
                word = random.choice(self.wordlist)
                if capitalize:
                    word = word.capitalize()
                words.append(word)

            passphrase = separator.join(words)
            self.pp_result_entry.setText(passphrase)
        except Exception:
            pass

    def copy_to_clipboard(self):
        pyperclip.copy(self.result_entry.text())
        self.copy_btn.setText("Copied!")
        QTimer.singleShot(2000, lambda: self.copy_btn.setText("Copy"))

    def copy_pp_to_clipboard(self):
        pyperclip.copy(self.pp_result_entry.text())
        self.pp_copy_btn.setText("Copied!")
        QTimer.singleShot(2000, lambda: self.pp_copy_btn.setText("Copy"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec())
