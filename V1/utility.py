import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QTextEdit, QPushButton, 
                             QLabel, QFileDialog, QMessageBox)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QSettings

class ObsidianSaverGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.loadSettings()

    def initUI(self):
        self.setWindowTitle('Obsidian Prompt Saver')
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Folder configuration
        folder_layout = QHBoxLayout()
        self.prompt_folder = QLineEdit()
        self.output_folder = QLineEdit()
        folder_layout.addWidget(QLabel('Prompts Folder:'))
        folder_layout.addWidget(self.prompt_folder)
        folder_layout.addWidget(QPushButton('Browse', clicked=lambda: self.browse_folder('prompt')))
        folder_layout.addWidget(QLabel('Outputs Folder:'))
        folder_layout.addWidget(self.output_folder)
        folder_layout.addWidget(QPushButton('Browse', clicked=lambda: self.browse_folder('output')))
        main_layout.addLayout(folder_layout)

        # Save Config button
        save_config_button = QPushButton('Save Config')
        save_config_button.clicked.connect(self.save_config)
        main_layout.addWidget(save_config_button)

        # Input fields
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText('Enter title')
        main_layout.addWidget(QLabel('Title:'))
        main_layout.addWidget(self.title_input)

        self.prompt_input = QTextEdit()
        self.prompt_input.setAcceptRichText(True)
        self.prompt_input.setPlaceholderText('Enter prompt')
        main_layout.addWidget(QLabel('Prompt:'))
        main_layout.addWidget(self.prompt_input)

        self.output_input = QTextEdit()
        self.output_input.setAcceptRichText(True)
        self.output_input.setPlaceholderText('Enter output')
        main_layout.addWidget(QLabel('Output:'))
        main_layout.addWidget(self.output_input)

        # Save button
        save_button = QPushButton('Save To Vault')
        save_button.clicked.connect(self.save_to_vault)
        main_layout.addWidget(save_button)

        # Terminal output
        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        main_layout.addWidget(QLabel('Status:'))
        main_layout.addWidget(self.terminal_output)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Set styles
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit, QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

    def browse_folder(self, folder_type):
        folder = QFileDialog.getExistingDirectory(self, f"Select {folder_type.capitalize()} Folder")
        if folder:
            if folder_type == 'prompt':
                self.prompt_folder.setText(folder)
            else:
                self.output_folder.setText(folder)

    def save_config(self):
        self.saveSettings()
        self.terminal_output.append("Configuration saved successfully.")

    def save_to_vault(self):
        title = self.title_input.text().strip()
        prompt = self.prompt_input.toPlainText()  # Keep all formatting
        output = self.output_input.toPlainText()  # Keep all formatting

        if not all([title, prompt, output, self.prompt_folder.text(), self.output_folder.text()]):
            QMessageBox.warning(self, "Input Error", "All fields must be filled and folders selected.")
            return

        try:
            # Save prompt file
            prompt_file_path = os.path.join(self.prompt_folder.text(), f"{title}.md")
            with open(prompt_file_path, 'w', encoding='utf-8') as f:
                f.write(prompt)  # Write prompt as-is

            # Save output file
            output_file_path = os.path.join(self.output_folder.text(), f"{title}.md")
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(f"# Prompt\n\n{prompt}\n\n# Output\n\n{output}\n\n")
                f.write(f"[[{os.path.basename(prompt_file_path)}]]")

            # Update prompt file with link to output
            with open(prompt_file_path, 'a', encoding='utf-8') as f:
                f.write(f"\n\n[[{os.path.basename(output_file_path)}]]")

            self.terminal_output.append(f"Successfully saved files for '{title}'")
            self.clear_inputs()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            self.terminal_output.append(f"Error: {str(e)}")

    def clear_inputs(self):
        self.title_input.clear()
        self.prompt_input.clear()
        self.output_input.clear()

    def loadSettings(self):
        settings = QSettings('ObsidianSaver', 'FolderSettings')
        self.prompt_folder.setText(settings.value('prompt_folder', ''))
        self.output_folder.setText(settings.value('output_folder', ''))

    def saveSettings(self):
        settings = QSettings('ObsidianSaver', 'FolderSettings')
        settings.setValue('prompt_folder', self.prompt_folder.text())
        settings.setValue('output_folder', self.output_folder.text())

def main():
    app = QApplication(sys.argv)
    ex = ObsidianSaverGUI()
    ex.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()