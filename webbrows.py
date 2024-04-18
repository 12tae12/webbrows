import sys
import subprocess
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import time
import os

install1 = ["pip", "install", "PyQt5"]
subprocess.call(install1)
install2 = ["pip", "install", "PyQtWebEngine"]
subprocess.call(install2)
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLineEdit, QListWidget, QListWidgetItem, QShortcut, QInputDialog, QTabWidget, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMessageBox, QTextEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl, QSettings, Qt
from PyQt5.QtGui import QKeySequence
import requests

install3 = ["pip", "install", "requests"]
subprocess.call(install3)
install4 = ["pip", "install", "mimetypes"]
subprocess.call(install4)
import mimetypes
print('dep install')
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

QToolBar {{
    background-color: {secondary};
    border: 2px solid {primary};
}}

QToolButton {{
    background-color: {secondary};
    border: none;
    padding: 8px 16px;
    color: {primary};
}}

QToolButton:hover {{
    background-color: {accent};
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

        # Define shortcut to open terminal
        self.terminal_shortcut = QShortcut(QKeySequence("Ctrl+Alt+T"), self)
        self.terminal_shortcut.activated.connect(self.open_terminal)

        self.load_tabs()

        self.new_tab_btn = QPushButton("+", self)
        navbar.addWidget(self.new_tab_btn)
        self.new_tab_btn.clicked.connect(self.new_tab_button_clicked)

        self.passwords_btn = QPushButton("Passwords", self)
        navbar.addWidget(self.passwords_btn)
        self.passwords_btn.clicked.connect(self.show_passwords)

        self.reload_app_btn = QPushButton("Reload App", self)
        navbar.addWidget(self.reload_app_btn)
        self.reload_app_btn.clicked.connect(self.reload_application)

        # Password manager window
        self.password_manager_window = PasswordManagerWindow()

        # Start monitoring the script file for changes
        self.start_file_monitor()

        # Apply Firefox-like stylesheet
        self.setStyleSheet(app_stylesheet)

    def start_file_monitor(self):
        event_handler = ScriptFileChangeHandler(self)
        observer = Observer()
        observer.schedule(event_handler, ".", recursive=False)
        observer.start()

    def show_restart_message(self):
        QMessageBox.information(self, "Script Updated", "The Python script has been updated. Please restart the browser to apply changes.", QMessageBox.Ok)

    def create_tab(self, url=None):
        webview = QWebEngineView()
        page = DownloadManager(webview)
        webview.setPage(page)
        if not url:  # If no URL is provided, navigate to the default home page
            url = "https://search.opensuse.org/"
        webview.load(QUrl.fromUserInput(url))
        close_btn = QPushButton("X")
        close_btn.clicked.connect(lambda: self.close_tab(webview))
        layout = QVBoxLayout()
        layout.addWidget(webview)
        layout.addWidget(close_btn)
        container = QWidget()
        container.setLayout(layout)
        self.tabs.addTab(container, "New Tab")
        self.tabs.setCurrentWidget(container)

    def close_tab(self, webview):
        index = self.tabs.indexOf(webview.parent())
        if index != -1:
            self.tabs.removeTab(index)

    def current_webview(self):
        widget = self.tabs.currentWidget()
        if isinstance(widget, QWidget):
            layout = widget.layout()
            if layout:
                return layout.itemAt(0).widget()
        return None

    def back_button_clicked(self):
        current_webview = self.current_webview()
        if current_webview:
            current_webview.back()

    def forward_button_clicked(self):
        current_webview = self.current_webview()
        if current_webview:
            current_webview.forward()

    def reload_button_clicked(self):
        current_webview = self.current_webview()
        if current_webview:
            current_webview.reload()

    def navigate_home(self):
        current_webview = self.current_webview()
        if current_webview:
            current_webview.load(QUrl("https://search.opensuse.org/"))

    def navigate_to_url(self):
        current_webview = self.current_webview()
        if current_webview:
            url = self.url_bar.text()
            if url.startswith("1t2://media"):
                self.load_local_file("music.html")
            elif url.startswith("1t2://game"):
                url = "https://1t2.pages.dev/tcrv"
            elif not url.startswith("http"):
                url = "http://" + url
            current_webview.load(QUrl(url))

    def update_url_bar(self, index):
        if index == self.tabs.indexOf(self.bookmarks_tab):
            self.url_bar.setText("")
        else:
            widget = self.tabs.widget(index)
            if isinstance(widget, QWidget):
                layout = widget.layout()
                if layout:
                    webview = layout.itemAt(0).widget()
                    if webview:
                        self.url_bar.setText(webview.url().toString())

    def add_bookmark(self):
        current_webview = self.current_webview()
        if current_webview:
            current_url = current_webview.url().toString()
            bookmark_title, ok = QInputDialog.getText(self, "Add Bookmark", "Enter bookmark title:")
            if ok:
                item = QListWidgetItem(bookmark_title, self.bookmarks_list)
                item.setData(Qt.UserRole, current_url)
                self.bookmarks_list.addItem(item)

    def load_bookmarks(self):
        # Load bookmarks from settings
        settings = QSettings("CustomWebBrowser", "Bookmarks")
        bookmarks = settings.value("bookmarks", [])
        for bookmark in bookmarks:
            item = QListWidgetItem(bookmark["title"], self.bookmarks_list)
            item.setData(Qt.UserRole, bookmark["url"])
            self.bookmarks_list.addItem(item)

    def save_bookmarks(self):
        # Save bookmarks to settings
        settings = QSettings("CustomWebBrowser", "Bookmarks")
        bookmarks = []
        for i in range(self.bookmarks_list.count()):
            item = self.bookmarks_list.item(i)
            title = item.text()
            url = item.data(Qt.UserRole)
            bookmarks.append({"title": title, "url": url})
        settings.setValue("bookmarks", bookmarks)

    def open_terminal(self):
        # Open the system terminal
        subprocess.Popen(['x-terminal-emulator'])

    def load_tabs(self):
        # Load saved tabs from settings
        settings = QSettings("CustomWebBrowser", "Tabs")
        tabs = settings.value("tabs", [])
        for tab in tabs:
            self.create_tab(tab["url"])

    def save_tabs(self):
        # Save tabs to settings
        settings = QSettings("CustomWebBrowser", "Tabs")
        tabs = []
        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)
            if isinstance(widget, QWidget):
                layout = widget.layout()
                if layout:
                    webview = layout.itemAt(0).widget()
                    if webview:
                        tabs.append({"url": webview.url().toString()})
        settings.setValue("tabs", tabs)

    def new_tab_button_clicked(self):
        self.create_tab()

    def show_passwords(self):
        self.password_manager_window.show()

    def reload_application(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def load_local_file(self, file_path):
        current_webview = self.current_webview()
        if current_webview:
            local_url = QUrl.fromLocalFile(file_path)
            current_webview.load(local_url)


class PasswordManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Password Manager")
        self.setGeometry(200, 200, 400, 300)

        self.passwords_textedit = QTextEdit()
        self.passwords_textedit.setReadOnly(True)
        self.setCentralWidget(self.passwords_textedit)

        show_passwords_btn = QPushButton("Show Passwords", self)
        show_passwords_btn.clicked.connect(self.show_all_passwords)

        add_password_btn = QPushButton("Add Password", self)
        add_password_btn.clicked.connect(self.add_password)

        toolbar = self.addToolBar("Toolbar")
        toolbar.addWidget(show_passwords_btn)
        toolbar.addWidget(add_password_btn)

        # Check if passwords file exists, if not, create it
        self.create_passwords_file()

    def create_passwords_file(self):
        try:
            with open("passwords.txt", "x"):
                pass
        except FileExistsError:
            pass

    def show_all_passwords(self):
        with open("passwords.txt", "r") as file:
            passwords = file.read()
        self.passwords_textedit.setPlainText(passwords)

    def add_password(self):
        site, ok = QInputDialog.getText(self, "Add Password", "Enter website/domain:")
        if ok and site:
            username, ok = QInputDialog.getText(self, "Add Password", "Enter username:")
            if ok and username:
                password, ok = QInputDialog.getText(self, "Add Password", "Enter password:", QLineEdit.Password)
                if ok and password:
                    with open("passwords.txt", "a") as file:
                        file.write(f"{site}: {username} - {password}\n")
                    QMessageBox.information(self, "Password Added", "Password added successfully.", QMessageBox.Ok)
                else:
                    QMessageBox.warning(self, "Error", "Password not provided.", QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "Error", "Username not provided.", QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Error", "Website/domain not provided.", QMessageBox.Ok)


class DownloadManager(QWebEnginePage):
    def __init__(self, view):
        super().__init__()
        self.view = view

    def acceptNavigationRequest(self, url, type, isMainFrame):
        if type == QWebEnginePage.NavigationTypeLinkClicked:
            if url.scheme() == "1t2" and url.path() == "/media":
                self.view.load_local_file("music.html")
                return False
            response = requests.head(url.toString())
            content_disposition = response.headers.get('Content-Disposition')
            if content_disposition and 'attachment' in content_disposition.lower():
                self.trigger_download(url, content_disposition)
                return False
        return super().acceptNavigationRequest(url, type, isMainFrame)

    def trigger_download(self, url, content_disposition):
        file_name = self.extract_file_name(content_disposition)
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self.view, "Save File", file_name, "All Files (*);;Text Files (*.txt)", options=options)
        if file_path:
            try:
                response = requests.get(url.toString())
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                QMessageBox.information(self.view, "Download Complete", "File downloaded successfully.", QMessageBox.Ok)
            except Exception as e:
                QMessageBox.warning(self.view, "Download Error", f"An error occurred while downloading the file: {str(e)}", QMessageBox.Ok)

    def extract_file_name(self, content_disposition):
        if 'filename=' in content_disposition:
            _, params = content_disposition.split(';', 1)
            for param in params.split(';'):
                key, value = param.strip().split('=', 1)
                if key == 'filename':
                    return value.strip("'\"")
        return "downloaded_file"


class ScriptFileChangeHandler(FileSystemEventHandler):
    def __init__(self, browser_window):
        super().__init__()
        self.browser_window = browser_window

    def on_modified(self, event):
        if event.src_path.endswith(".py") and event.src_path == __file__:
            self.browser_window.show_restart_message()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())
