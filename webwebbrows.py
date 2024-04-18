import subprocess
from flask import Flask, request, jsonify, render_template
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLineEdit, QListWidget, QListWidgetItem, QPushButton, QMessageBox, QTextEdit, QFileDialog, QVBoxLayout, QWidget, QInputDialog, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, QSettings, Qt
from PyQt5.QtGui import QKeySequence
import requests

install1 = ["pip", "install", "PyQt5"]
subprocess.call(install1)
install2 = ["pip", "install", "PyQtWebEngine"]
subprocess.call(install2)
install3 = ["pip", "install", "requests"]
subprocess.call(install3)
install4 = ["pip", "install", "mimetypes"]
subprocess.call(install4)

app = Flask(__name__)

# Define Firefox-like color palette
firefox_colors = {
    "primary": "#ffffff",  # White text color
    "secondary": "#2b2b2b",  # Dark gray background
    "highlight": "#ffc859",  # Yellowish highlight color
    "accent": "#28a745",  # Green accent color
}

# Apply Firefox-like styles to UI elements
app_stylesheet = """
QTabBar::tab {{
    background-color: {secondary};
    color: {primary};
    border: 2px solid {secondary};
    padding: 8px;
}}

QTabBar::tab:selected {{
    background-color: {primary};
    border-bottom: none;
}}

QTabBar::tab:hover {{
    background-color: {accent};
}}

QTabBar::tab:first {{
    background-color: {highlight}; /* Set a different color for the bookmarks tab */
}}

QTabBar::tab:selected {{
    background-color: {accent}; /* Set a different color for the selected tab */
}}

QTabBar::tab:selected:hover {{
    background-color: {accent}; /* Keep the color consistent on hover */
}}

QLineEdit {{
    background-color: {secondary};
    border: 2px solid {primary};
    color: {primary};
    padding: 6px;
}}

QPushButton {{
    background-color: {secondary};  /* Darker background color */
    border: none;
    color: {primary};
    padding: 8px 16px;
}}

QPushButton:hover {{
    background-color: {primary};
}}
""".format(**firefox_colors)

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Web Browser")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.bookmarks_tab = QWidget()
        self.bookmarks_layout = QVBoxLayout()
        self.bookmarks_list = QListWidget()
        self.bookmarks_tab.setLayout(self.bookmarks_layout)
        self.bookmarks_layout.addWidget(self.bookmarks_list)
        self.tabs.addTab(self.bookmarks_tab, "Bookmarks")

        self.load_bookmarks()

        navbar = self.addToolBar("Navigation")

        back_btn = QAction("Back", self)
        navbar.addAction(back_btn)
        back_btn.triggered.connect(self.back_button_clicked)

        forward_btn = QAction("Forward", self)
        navbar.addAction(forward_btn)
        forward_btn.triggered.connect(self.forward_button_clicked)

        reload_btn = QAction("Reload", self)
        navbar.addAction(reload_btn)
        reload_btn.triggered.connect(self.reload_button_clicked)

        home_btn = QAction("Home", self)
        navbar.addAction(home_btn)
        home_btn.triggered.connect(self.navigate_home)

        bookmark_btn = QAction("Bookmark", self)
        navbar.addAction(bookmark_btn)
        bookmark_btn.triggered.connect(self.add_bookmark)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        self.tabs.currentChanged.connect(self.update_url_bar)

        # Apply Firefox-like stylesheet
        self.setStyleSheet(app_stylesheet)

    def back_button_clicked(self):
        # Handle back button click
        pass

    def forward_button_clicked(self):
        # Handle forward button click
        pass

    def reload_button_clicked(self):
        # Handle reload button click
        pass

    def navigate_home(self):
        # Handle navigate home button click
        pass

    def navigate_to_url(self):
        # Handle navigate to URL
        pass

    def update_url_bar(self, index):
        # Handle update URL bar
        pass

    def add_bookmark(self):
        # Handle add bookmark
        pass

    def load_bookmarks(self):
        # Handle load bookmarks
        pass

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
