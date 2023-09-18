import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QTextEdit,
    QFileDialog, QScrollArea, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QIcon, QPixmap, QFont, QPalette, QColor, QImage, QCursor, QPainter
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

from QuizGenerator import generate_java_oop_mcqs

def get_resource_path(filename):
    """Get the absolute path to a resource file."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

class TitleLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.shadow_color = QColor(0, 0, 0, 100)
        self.text_color = QColor(221, 221, 221)
        self.setFont(QFont("Arial", 24, QFont.Bold))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        
        # Draw the shadow text
        shadow_rect = self.rect().translated(2, 2)
        painter.setPen(self.shadow_color)
        painter.drawText(shadow_rect, self.alignment(), self.text())
        
        # Draw the main text
        painter.setPen(self.text_color)
        painter.drawText(self.rect(), self.alignment(), self.text())

class MCQGeneratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MCQ Generator")
        self.setGeometry(230, 100, 800, 600)
        self.setStyleSheet(
            "QMainWindow { background-color: #000; }"
        )

        self.setWindowIcon(get_icon())

        font = QFont("Arial", 12)
        QApplication.setFont(font)

        # Create widgets
        self.text_file_button = QPushButton("Select Text File")
        self.text_file_button.clicked.connect(self.select_text_file)
        self.text_file_button.setStyleSheet(
            "QPushButton { font-weight: bold; font-size: 16px; background-color: #222; color: #fff; border-radius: 10px; border: 2px solid #555; }"
            "QPushButton:hover { background-color: #333; border: 2px solid #777; }"
            "QPushButton:pressed { background-color: #111; border: 2px solid #444; }"
        )
        self.text_file_button.setCursor(QCursor(Qt.PointingHandCursor))

        self.text_file_path_label = QLabel()
        self.text_file_path_label.setStyleSheet("QLabel { color: #fff; font-weight: bold; font-size: 14px; }")

        self.generate_button = QPushButton("Generate MCQs")
        self.generate_button.clicked.connect(self.generate_mcqs)
        self.generate_button.setStyleSheet(
            "QPushButton { font-weight: bold; font-size: 16px; background-color: #222; color: #fff; border-radius: 10px; border: 2px solid #555; }"
            "QPushButton:hover { background-color: #333; border: 2px solid #777; }"
            "QPushButton:pressed { background-color: #111; border: 2px solid #444; }"
        )
        self.generate_button.setCursor(QCursor(Qt.PointingHandCursor))

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_text_file)
        self.download_button.setStyleSheet(
            "QPushButton { font-weight: bold; font-size: 16px; background-color: #e74c3c; color: #fff; border-radius: 10px; border: 2px solid #c0392b; }"
            "QPushButton:hover { background-color: #c0392b; border: 2px solid #a5291e; }"
            "QPushButton:pressed { background-color: #922b21; border: 2px solid #811f17; }"
        )
        self.download_button.setCursor(QCursor(Qt.PointingHandCursor))

        self.result_text_edit = QTextEdit()
        self.result_text_edit.setStyleSheet("QTextEdit { color: #fff; font-weight: bold; font-size: 14px; background-color: #000; }")
        self.result_text_edit.setReadOnly(True)

        layout = QVBoxLayout()
        title_label = TitleLabel("MCQ Generator")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(self.text_file_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.text_file_path_label, alignment=Qt.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(self.generate_button, alignment=Qt.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(self.download_button, alignment=Qt.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(self.result_text_edit)

        layout_widget = QWidget(self)
        layout_widget.setLayout(layout)
        layout_widget.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        layout_widget.setGeometry(200, 100, 400, 400)

        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        scroll_area.setGeometry(0, 0, 800, 600)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(layout_widget)
        self.setCentralWidget(scroll_area)

        self.keyword_file_path = "list.json"

        # Add a shadow effect to buttons
        self.add_shadow_effect(self.text_file_button)
        self.add_shadow_effect(self.generate_button)
        self.add_shadow_effect(self.download_button)

    def add_shadow_effect(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(255, 255, 255, 50))
        shadow.setOffset(5, 5)
        widget.setGraphicsEffect(shadow)

    def select_text_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Text File", "", "Text Files (*.txt)", options=options)
        if file_path:
            self.text_file_path_label.setText(file_path)

    def generate_mcqs(self):
        text_file_path = self.text_file_path_label.text()

        try:
            mcqs = generate_java_oop_mcqs(text_file_path, self.keyword_file_path)
            self.display_result(mcqs)
        except Exception as e:
            self.display_result(str(e))

    def display_result(self, result):
        output = ""
        for idx, mcq in enumerate(result):
            output += f"MCQ {idx+1}:\n"
            output += f"Question: {mcq['question']}\n"
            output += "Choices:\n"
            for i, choice in enumerate(mcq['choices']):
                output += f"{chr(ord('A') + i)}) {choice}\n"
            output += f"Correct Option: {mcq['correct_option']}\n\n"

        self.result_text_edit.setStyleSheet("QTextEdit { color: #fff; font-weight: bold; font-size: 14px; background-color: #000; }")
        self.result_text_edit.setText(output)

    def download_text_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Text File", "", "Text Files (*.txt)", options=options)
        if save_path:
            with open(save_path, 'w') as file:
                file.write(self.result_text_edit.toPlainText())

def get_icon():
    icon = QtGui.QIcon(get_resource_path('icon.png'))
    return icon

if __name__ == '__main__':
    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(0, 0, 0))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(0, 0, 0))
    palette.setColor(QPalette.AlternateBase, QColor(40, 40, 40))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(0, 0, 0))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    
    app.setPalette(palette)

    mcq_generator = MCQGeneratorGUI()
    mcq_generator.show()
    sys.exit(app.exec_())
