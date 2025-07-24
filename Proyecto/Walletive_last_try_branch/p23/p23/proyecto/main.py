import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import Walletive  # o como se llame tu ventana principal

if __name__ == "__main__":
    app = QApplication(sys.argv) 
    ventana = Walletive()
    ventana.show()
    sys.exit(app.exec_())