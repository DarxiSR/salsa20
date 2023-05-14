try:
    import sys
except Exception:
    raise ImportError('[-] Ошибка импортирования библиотеки sys!\n')
try:
    import GUI
except Exception:
    raise ImportError('[-] Ошибка импортирования библиотеки GUI!\n')
try:
    from Salsa20 import Salsa20
except Exception:
    raise ImportError('[-]  Ошибка импортирования библиотеки Salsa20!\n')
try:
    from PyQt5 import QtWidgets
except Exception:
    raise ImportError('[-]  Ошибка импортирования библиотеки PyQt5!\n')

class __core(QtWidgets.QMainWindow, GUI.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.__encrypt)
        self.pushButton_2.clicked.connect(self.__decrypt)

    def __encrypt(self):
        set_encryption_key = self.lineEdit.text()
        set_cryptographic_nonce = self.lineEdit_2.text()
        set_cryptographic_thread_position = self.lineEdit_3.text()
        set_nothing_up_my_sleeve_number = self.lineEdit_4.text()
        set_input_text = self.lineEdit_5.text()

        try:
            if len(set_encryption_key) != int(64):
                self.lineEdit.setText('Ошибка значений!\n')
            elif len(set_cryptographic_nonce) != int(16):
                self.lineEdit2.setText('Ошибка значений!\n')
            elif len(set_cryptographic_thread_position) != int(16):
                self.lineEdit3.setText('Ошибка значений!\n')
            elif len(set_nothing_up_my_sleeve_number) != int(32):
                self.lineEdit4.setText('Ошибка значений!\n')
            else:
                get_cipher = Salsa20(set_encryption_key, set_cryptographic_nonce, set_cryptographic_thread_position, set_nothing_up_my_sleeve_number)
                get_result = get_cipher.salsa_20_encryption(set_input_text)
                self.lineEdit_6.setText(get_result)
        except Exception:
            raise BufferError('[-] Ошибка буффера памяти при инициализации переменных!\n')

    def __decrypt(self):
        set_encryption_key = self.lineEdit.text()
        set_cryptographic_nonce = self.lineEdit_2.text()
        set_cryptographic_thread_position = self.lineEdit_3.text()
        set_nothing_up_my_sleeve_number = self.lineEdit_4.text()
        set_input_text = self.lineEdit_5.text()

        try:
            if len(set_encryption_key) != int(64):
                self.lineEdit.setText('Ошибка значений!\n')
            elif len(set_cryptographic_nonce) != int(16):
                self.lineEdit2.setText('Ошибка значений!\n')
            elif len(set_cryptographic_thread_position) != int(16):
                self.lineEdit3.setText('Ошибка значений!\n')
            elif len(set_nothing_up_my_sleeve_number) != int(32):
                self.lineEdit4.setText('Ошибка значений!\n')
            else:
                get_cipher = Salsa20(set_encryption_key, set_cryptographic_nonce, set_cryptographic_thread_position,set_nothing_up_my_sleeve_number)
                get_result = get_cipher.salsa_20_decryption(set_input_text)

                self.lineEdit_6.setText(get_result)
        except Exception:
            raise BufferError('[-] Ошибка буффера памяти при инициализации переменных!\n')

def __gui():
    get_application = QtWidgets.QApplication(sys.argv)
    get_hdwid = __core()
    get_hdwid.show()
    get_application.exec_()

if __name__ == '__main__':
    try:
        __gui()
    except:
        raise BufferError('[-] Ошибка в main функции!\n')
