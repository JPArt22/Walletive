from gui.main_window import Walletive

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ventana = Walletive()
    ventana.show()
    sys.exit(app.exec_())
