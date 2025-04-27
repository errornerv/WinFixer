import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout,
    QWidget, QMessageBox
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
from core import fixer, permissions, logger


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WinFixer - Windows Repair Tool")
        self.setGeometry(300, 150, 500, 600)

        app_font = QFont("Arial", 12)
        self.setFont(app_font)

        self.setStyleSheet(self.load_dark_theme())
        self.init_ui()

        if not permissions.is_user_admin():
            self.show_permission_error()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🛠️ Windows Repair Tool")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        btn_network = QPushButton("🔄 Reset Network Settings")
        btn_network.clicked.connect(self.handle_reset_network)

        btn_icon_cache = QPushButton("🧹 Clear Icon Cache")
        btn_icon_cache.clicked.connect(self.handle_clear_icons)

        btn_temp_files = QPushButton("🗑️ Delete Temporary Files")
        btn_temp_files.clicked.connect(self.handle_delete_temp_files)

        btn_disk_cleanup = QPushButton("💾 Disk Cleanup")
        btn_disk_cleanup.clicked.connect(self.handle_disk_cleanup)

        btn_sfc_scan = QPushButton("🔍 Run SFC Scan")
        btn_sfc_scan.clicked.connect(self.handle_sfc_scan)

        self.restart_button = QPushButton("🔄 Restart Computer")
        self.restart_button.clicked.connect(self.handle_restart)
        self.restart_button.setMinimumHeight(40)
        self.restart_button.setCursor(Qt.PointingHandCursor)
        self.restart_button.setVisible(False)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)

        for btn in [btn_network, btn_icon_cache, btn_temp_files, btn_disk_cleanup, btn_sfc_scan]:
            btn.setMinimumHeight(40)
            btn.setCursor(Qt.PointingHandCursor)

        layout.addWidget(title)
        layout.addWidget(btn_network)
        layout.addWidget(btn_icon_cache)
        layout.addWidget(btn_temp_files)
        layout.addWidget(btn_disk_cleanup)
        layout.addWidget(btn_sfc_scan)
        layout.addWidget(self.restart_button)
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def handle_reset_network(self):
        self.status_label.setText("⏳ Resetting network settings...")
        self.restart_button.setVisible(False)
        QApplication.processEvents()
        if not permissions.is_user_admin():
            self.status_label.setText("❌ Please run the app as Administrator.")
            return
        success, restart_required = fixer.reset_network_adapter()
        if success:
            if restart_required:
                self.status_label.setText("✅ Network reset successfully. Please restart your computer.")
                self.restart_button.setVisible(True)
            else:
                self.status_label.setText("✅ Network reset successfully.")
        else:
            self.status_label.setText("❌ Failed to reset network. Check logs for details.")

    def handle_clear_icons(self):
        self.status_label.setText("⏳ Clearing icon cache...")
        self.restart_button.setVisible(False)
        QApplication.processEvents()
        success, restart_required = fixer.clear_icon_cache()
        if success:
            if restart_required:
                self.status_label.setText("✅ Icon cache cleared successfully. Explorer was restarted.")
            else:
                self.status_label.setText("✅ Icon cache cleared successfully.")
        else:
            self.status_label.setText("❌ Failed to clear icon cache.")

    def handle_delete_temp_files(self):
        self.status_label.setText("⏳ Deleting temporary files...")
        self.restart_button.setVisible(False)
        QApplication.processEvents()
        if fixer.delete_temp_files():
            self.status_label.setText("✅ Temporary files deleted successfully.")
        else:
            self.status_label.setText("❌ Failed to delete temporary files.")

    def handle_disk_cleanup(self):
        self.status_label.setText("⏳ Running disk cleanup...")
        self.restart_button.setVisible(False)
        QApplication.processEvents()
        if fixer.disk_cleanup():
            self.status_label.setText("✅ Disk cleanup completed successfully.")
        else:
            self.status_label.setText("❌ Disk cleanup failed.")

    def handle_sfc_scan(self):
        self.status_label.setText("⏳ Running SFC scan...")
        self.restart_button.setVisible(False)
        QApplication.processEvents()
        if fixer.run_sfc_scan():
            self.status_label.setText("✅ SFC scan completed successfully.")
        else:
            self.status_label.setText("❌ SFC scan failed.")

    def handle_restart(self):
        try:
            os.system("shutdown /r /t 0")
        except Exception as e:
            logger.log(f"Failed to initiate restart: {e}", level="error")
            self.status_label.setText("❌ Failed to restart. Please restart manually.")

    def show_permission_error(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Permission Error")
        msg.setText("Please run the app as Administrator.")
        msg.setIcon(QMessageBox.Critical)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: Arial;
                font-size: 14px;
            }
            QPushButton {
                background-color: #444;
                color: white;
                border-radius: 6px;
                padding: 6px 15px;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        msg.exec()
        sys.exit()

    def load_dark_theme(self):
        return """
            QMainWindow {
                background-color: #1e1e1e;
                color: #f0f0f0;
            }
            QPushButton {
                background-color: #333;
                color: #f0f0f0;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #444;
            }
            QLabel {
                color: #f0f0f0;
            }
        """