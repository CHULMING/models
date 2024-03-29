import sys
import os
import time
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from RestApi import post_data

TR_INTERVAL = 0.2

class Kiwoom(QAxWidget):
    def __init__(self, sRQName):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()
        self.comm_connect()

        self.sRQName = sRQName

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
    
    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)
        self.OnReceiveChejanData.connect(self._receive_chejan_data)
    
    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print('connected')
        else:
            print('disconnected')
        
        self.login_event_loop.exit()

    def get_login_info(self, tag):
        ret = self.dynamicCall("GetLoginInfo(QString)", tag)
        return ret

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def get_connect_state(self):
        ret = self.dynamicCall("GetConnectState()")
        return ret
    
    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QSting, QSting, int, QSting)", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1,
                         unused2, unused3, unused4):
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False
        
        if rqname == 'opt10081_req':
            self._opt10081(rqname, trcode)
        elif rqname == 'opt10080_req':
            self._opt10080(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass
    
    def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",
                          [self.sRQName, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no])

    def get_chejan_data(self, fid):
        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret

    def _receive_chejan_data(self, gubun, item_cnt, fid_list):
        print(gubun)
        print(self.get_chejan_data(9203))
        print(self.get_chejan_data(302))
        print(self.get_chejan_data(900))
        print(self.get_chejan_data(901))

    def _opt10080(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)
        payload_data = {}
        # data_cnt = 0
        for i in range(data_cnt):
            payload_data['code'] = self.code
            payload_data['open'] = int(self._comm_get_data(trcode, "", rqname, i, "시가"))
            payload_data['close'] = int(self._comm_get_data(trcode, "", rqname, i, "현재가"))
            payload_data['low'] = int(self._comm_get_data(trcode, "", rqname, i, "저가"))
            payload_data['high'] = int(self._comm_get_data(trcode, "", rqname, i, "고가"))
            payload_data['volume'] = int(self._comm_get_data(trcode, "", rqname, i, "거래량"))
            date  = self._comm_get_data(trcode, "", rqname, i, "체결시간")[:-2]
            payload_data['date'] = time[:4] + '-' + date[4:6] + '-' + date[6:8] + 'T'+ date[8:10] + ':' + date[10:12]
            # post_data(payload_data, type='minute')
        print('done ' + rqname + '  ' +trcode)
    
    def _opt10081(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)
        payload_data = {}
        # data_cnt = 0
        for i in range(data_cnt):
            time.sleep(0.1)
            payload_data['code'] = self.code
            payload_data['open'] = int(self._comm_get_data(trcode, "", rqname, i, "시가"))
            payload_data['close'] = int(self._comm_get_data(trcode, "", rqname, i, "현재가"))
            payload_data['low'] = int(self._comm_get_data(trcode, "", rqname, i, "저가"))
            payload_data['high'] = int(self._comm_get_data(trcode, "", rqname, i, "고가"))
            payload_data['volume'] = int(self._comm_get_data(trcode, "", rqname, i, "거래량"))
            date  = self._comm_get_data(trcode, "", rqname, i, "일자")
            payload_data['date'] = date[:4] + '-' + date[4:6] + '-' + date[6:8]
            #print(payload_data)
            post_data(payload_data, type='day')
        print('done ' + rqname + '  ' +trcode)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    k = Kiwoom()
    k.comm_connect()
    print(k.get_connect_state())
    k.rq_minute_data(code='005930')