import sys
from PyQt5.QtWidgets import *
# from PyQt5.QAxContainer import *
# from PyQt5.QtCore import *
from Kiwoom import Kiwoom

if __name__ == "__main__":
    app = QApplication(sys.argv)
    k = Kiwoom()
    k.comm_connect()
    print(k.get_connect_state())
    #k.rq_minute_data(code='069500')
    k.rq_day_data(code='005930')