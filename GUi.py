import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QTextEdit, QFileDialog, QMessageBox, QScrollArea
from PyQt5.QtGui import QIcon, QPixmap, QFont, QPalette, QColor, QPainter, QBrush, QPen, QPolygon
from PyQt5.QtCore import Qt, QPoint
import os

from PyQt5 import QtGui

from QuizGenerator import generate_java_oop_mcqs

def get_resource_path(filename):
    """Get the absolute path to a resource file."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

class MCQGeneratorGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MCQ Generator")
        self.setGeometry(230, 100, 800, 600)  # Increased window size
        self.setStyleSheet("QMainWindow::title { background-color: #FF0000;font-size: 16px}")

        # Set application icon
        self.setWindowIcon(get_icon())

        # Set the font for the application
        font = QFont("Arial", 12)  # Change the font name and size as desired
        QApplication.setFont(font)

        # Create widgets
        self.text_file_button = QPushButton("Select Text File")
        self.text_file_button.clicked.connect(self.select_text_file)
        self.text_file_button.setStyleSheet("QPushButton { font-weight: bold; font-size: 16px; background-color: #4CAF50; color: white; }"
                                             "QPushButton:hover { background-color: #45a049; }"
                                             "QPushButton:pressed { background-color: #379946; }")

        self.text_file_path_label = QLabel()
        self.text_file_path_label.setStyleSheet("QLabel { color: white; font-weight: bold; font-size: 16px; }")

        self.generate_button = QPushButton("Generate MCQs")
        self.generate_button.clicked.connect(self.generate_mcqs)
        self.generate_button.setStyleSheet("QPushButton { font-weight: bold; font-size: 16px; background-color: #4CAF50; color: white; }"
                                            "QPushButton:hover { background-color: #45a049; }"
                                            "QPushButton:pressed { background-color: #379946; }")
        self.generate_button.setMaximumHeight(60)  # Increased height for better visibility

        self.result_text_edit = QTextEdit()
        self.result_text_edit.setStyleSheet("QTextEdit { color: black; font-weight: bold; font-size: 16px; }")
        self.result_text_edit.setReadOnly(True)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("MCQ Generator", alignment=Qt.AlignCenter))
        layout.addSpacing(40)  # Increased spacing between widgets
        layout.addWidget(self.text_file_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.text_file_path_label, alignment=Qt.AlignCenter)
        layout.addSpacing(40)
        layout.addWidget(self.generate_button, alignment=Qt.AlignCenter)
        layout.addSpacing(40)
        layout.addWidget(self.result_text_edit)

        # Set background image
        self.background_image = QPixmap("img.jpg")
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, 800, 600)  # Adjusted geometry to match window size
        self.background_label.setAlignment(Qt.AlignCenter)
        self.background_label.setPixmap(self.background_image)

        # Set transparent background for layout
        layout_widget = QWidget(self)
        layout_widget.setLayout(layout)
        layout_widget.setStyleSheet("background-color: rgba(0, 0, 0, 0);")  # Set transparent background
        layout_widget.setGeometry(200, 100, 400, 400)  # Adjusted geometry to match window size

        # Add scroll area to the layout widget
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        scroll_area.setGeometry(0, 0, 800, 600)  # Adjusted geometry to match window size
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(layout_widget)
        self.setCentralWidget(scroll_area)

        # Set default JSON file path
        self.keyword_file_path = "list.json"

    def select_text_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Text File", "", "Text Files (*.txt)", options=options)
        if file_path:
            self.text_file_path_label.setText(file_path)

    def generate_mcqs(self):
        text_file_path = self.text_file_path_label.text()

        # Generate MCQs
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

        # Update text color, font size, and font weight
        self.result_text_edit.setStyleSheet("QTextEdit { color: white; font-weight: bold; font-size: 16px; background-color: rgba(0, 0, 0, 0); }")

        self.result_text_edit.setText(output)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        brush = QBrush(Qt.black, Qt.Dense7Pattern)
        painter.setPen(QPen(Qt.white))
        painter.setBrush(brush)
        painter.drawRect(self.rect())

        # Draw background image
        scaled_image = self.background_image.scaled(self.background_label.size(), Qt.AspectRatioMode.IgnoreAspectRatio)
        painter.drawPixmap(self.background_label.rect(), scaled_image)


def get_icon():
    icon = QtGui.QIcon(get_resource_path('icon.png'))
    return icon


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Set the global style for the application
    app.setStyle("Fusion")

    # Set the palette colors for the application
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(0, 0, 0, 0))  # Set transparent background
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(0, 0, 0, 0))  # Set transparent background
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.white)
    
    app.setPalette(palette)

    mcq_generator = MCQGeneratorGUI()
    mcq_generator.show()
    sys.exit(app.exec_())
