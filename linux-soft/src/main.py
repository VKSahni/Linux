import sys
import subprocess
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox, QProgressBar


class SystemControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Control")
        self.setGeometry(100, 100, 300, 250)
        self.setStyleSheet("background-color: #f0f0f0;")

        # Create buttons with animations
        self.shutdown_button = self.create_button("Shutdown", "icons/shutdown.png", self.shutdown)
        self.reboot_button = self.create_button("Reboot", "icons/reboot.png", self.reboot)
        self.update_button = self.create_button("Update", "icons/update.png", self.update_system)
        self.upgrade_button = self.create_button("Upgrade", "icons/upgrade.png", self.upgrade_system)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.shutdown_button)
        layout.addWidget(self.reboot_button)
        layout.addWidget(self.update_button)
        layout.addWidget(self.upgrade_button)

        self.setLayout(layout)

    def create_button(self, text, icon_path, action):
        """Create a styled button with an icon and animation."""
        button = QPushButton(text)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(30, 30))  # Fix for the QSize issue
        button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        button.clicked.connect(action)
        
        # Add hover animation
        self.add_hover_animation(button)
        
        return button

    def add_hover_animation(self, button):
        """Add hover effect to buttons."""
        animation = QPropertyAnimation(button, b"color")
        animation.setDuration(400)
        animation.setStartValue(QColor(76, 175, 80))  # Green color
        animation.setEndValue(QColor(67, 160, 71))    # Darker green
        button.enterEvent = lambda event: animation.start()
        button.leaveEvent = lambda event: animation.setDirection(QPropertyAnimation.Backward) or animation.start()

    def show_message(self, title, message):
        """Display a confirmation dialog."""
        response = QMessageBox.question(self, title, message, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        return response == QMessageBox.Yes

    def shutdown(self):
        if self.show_message("Shutdown", "Are you sure you want to shut down?"):
            self.run_command(["sudo", "shutdown", "-h", "now"])

    def reboot(self):
        if self.show_message("Reboot", "Are you sure you want to reboot?"):
            self.run_command(["sudo", "reboot"])

    def update_system(self):
        if self.show_message("Update", "Are you sure you want to update the system?"):
            self.run_command_with_progress(["sudo", "apt", "update"])

    def upgrade_system(self):
        if self.show_message("Upgrade", "Are you sure you want to upgrade the system?"):
            self.run_command_with_progress(["sudo", "apt", "upgrade", "-y"])

    def run_command(self, command):
        """Run system command without feedback."""
        subprocess.run(command)

    def run_command_with_progress(self, command):
        """Run command with a progress bar animation."""
        progress_bar = QProgressBar(self)
        progress_bar.setRange(0, 100)
        progress_bar.setValue(0)
        progress_bar.setGeometry(50, 150, 200, 25)
        progress_bar.show()

        # Start the progress bar animation
        self.animate_progress(progress_bar)

        # Simulate running the command (you can integrate actual progress tracking here)
        subprocess.run(command)

        progress_bar.hide()

    def animate_progress(self, progress_bar):
        """Animate the progress bar."""
        animation = QPropertyAnimation(progress_bar, b"value")
        animation.setDuration(3000)  # Set duration of the progress animation (3 seconds)
        animation.setStartValue(0)
        animation.setEndValue(100)
        animation.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemControlApp()
    window.show()
    sys.exit(app.exec_())
