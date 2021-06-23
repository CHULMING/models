import sys
import os
import time
from PyQt5.QtWidgets import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Kiwoom import Kiwoom


'''
 BSTR sRQName, // 사용자 구분명
          BSTR sScreenNo, // 화면번호
          BSTR sAccNo,  // 계좌번호 10자리 맨 뒤에 11 붙여줘서 10자리 만들어줘야 함
          LONG nOrderType,  // 주문유형 1:신규매수, 2:신규매도 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정
          BSTR sCode, // 종목코드 (6자리)
          LONG nQty,  // 주문수량
          LONG nPrice, // 주문가격
          BSTR sHogaGb,   // 거래구분(혹은 호가구분)은 아래 참고
          BSTR sOrgOrderNo  // 원주문번호. 신규주문에는 공백 입력, 정정/취소시 입력합니다.
'''

class KiwoomWrapper(Kiwoom):
    sRQName = 1
    def __init__(self):
        super().__init__(KiwoomWrapper.sRQName)
        KiwoomWrapper.sRQName = KiwoomWrapper.sRQName + 1


    def get_data_from_kiwoom(self, code, type='day'): # get data and save to DB
        self.code = code
        self.set_input_value('종목코드', self.code)
        self.set_input_value('틱범위', '1')
        self.set_input_value('수정주가구분', '0')
        
        if type == 'minute':
            self.comm_rq_data('opt10080_req', 'opt10080', 0, '2000')
            for i in range(0):
                time.sleep(0.2)
                self.set_input_value('종목코드', self.code)
                self.set_input_value('틱범위', '1')
                self.set_input_value('수정주가구분', '0')
                self.comm_rq_data('opt10080_req', 'opt10080', 2, "2000")
        
        elif type == 'day':
            self.set_input_value('기준일자', '20210525')
            self.comm_rq_data('opt10081_req', 'opt10081', 0, "2001")
