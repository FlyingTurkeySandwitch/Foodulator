import sys
from PySide6.QtWidgets import QApplication
from gui.response_app import ResponseApp
from DB.DB_manager import initialize_database

if __name__ == "__main__":
    initialize_database()
    app = QApplication(sys.argv)
    window = ResponseApp()
    window.show()
    sys.exit(app.exec())

