import sys
import os
import time
#sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from PyQt5.QtWidgets import *
from KiwoomWrapper import KiwoomWrapper

if __name__ == "__main__":
    app = QApplication(sys.argv)
    k = KiwoomWrapper()     
    
    # k.get_data(code='005930', type='minute')
    # k.send_order('1', '1999', '8167335311', 1, '005930', 1, 0, '03', '')


    # get함수 인데 리턴을 못해...