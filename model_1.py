from RestApi import get_data

BAEK = 1000000
CHON = 10000000
YEOK = 100000000
DAY5 = 0
DAY10 = 1
DAY15 = 2
DAY30 = 3
DAY60 = 4
DAY120 = 5


class ModelBasic:

    def __init__(self, deposit, code, type):
        self.capital = deposit
        self.deposit = deposit
        self.code = code
        self.type = type
        self.price_data = get_data(code=self.code, type=type)
        print(len(self.price_data))
        self.stock = {self.code : 0, 'avg_price' : 0}  # '005930' : '5' -> Bought Samsung 5EA
        self.MA_line = [0, 0, 0, 0, 0, 0]  # 5, 10, 15, 30, 60, 120

    def pre_processing(self):
        self.price_by_date = []
        for data in reversed(self.price_data):
            if self.type == 'day':
                data['date'] = data['date'][:10]
            self.price_by_date.append({'open': data['open'], 'close': data['close'], 'date':data['date']})
        for i in range(120):
            self.MA_line[DAY120] = self.MA_line[DAY120] + self.price_by_date[i]['close']
        for i in range(60):
            self.MA_line[DAY60] = self.MA_line[DAY60] + self.price_by_date[i]['close']
        for i in range(30):
            self.MA_line[DAY30] = self.MA_line[DAY30] + self.price_by_date[i]['close']
        for i in range(15):
            self.MA_line[DAY15] = self.MA_line[DAY15] + self.price_by_date[i]['close']            
        for i in range(10):
            self.MA_line[DAY10] = self.MA_line[DAY10] + self.price_by_date[i]['close']
        for i in range(5):
            self.MA_line[DAY5] = self.MA_line[DAY5] + self.price_by_date[i]['close']

    def buy(self, data, division=1):
        if self.deposit < data['close']:
            return
        budget = self.deposit * division
        amount = int(budget/data['close'])
        self.stock[self.code] = self.stock[self.code] + amount
        self.stock['avg_price'] = data['close']
        self.deposit = self.deposit - (amount * data['close'])

        print('[Buy] {} // price : {}, amount : {}'.format(data['date'], data['close'], amount))
#        print('Status // Deposit : {}, Stock : {}'.format(self.deposit, self.stock[self.code]))

    def sell(self, data, division=1):
        if self.stock[self.code] == 0:
            return
        amount = self.stock[self.code] * division
        revenue = (data['close'] - self.stock['avg_price']) * self.stock[self.code]
        self.stock[self.code] = self.stock[self.code] - amount
        self.stock['avg_price'] = 0 # division에 따라 수정되어야 함
        self.deposit = self.deposit + (data['close'] * amount)
        print('[Sell] {} // price : {}, amount : {} => Revenue {}\n'.format(data['date'], data['close'], amount, revenue))
#        print('Status // Deposit : {}, Stock : {}'.format(self.deposit, self.stock[self.code]))
        
    def run(self):
        self.pre_processing()

        for i in range(5,len(self.price_by_date)):
            yesterday_data = self.price_by_date[i-1]
            today_data = self.price_by_date[i]
            self.MA_line[DAY5] = self.MA_line[DAY5] - self.price_by_date[i-5]['close'] + today_data['close']
            MA_line_5 = self.MA_line[DAY5] / 5

            # print(MA_line_5, today_data['open'], today_data['close'])
            if yesterday_data['close'] < MA_line_5 and \
               today_data['open'] > MA_line_5 and \
               today_data['close'] > today_data['open']:
                self.buy(today_data)
            elif today_data['open'] < MA_line_5 and today_data['close'] > MA_line_5:
                self.buy(today_data)
            elif yesterday_data['close'] > MA_line_5 and \
                today_data['open'] < MA_line_5 and \
                today_data['close'] < today_data['close']:
                self.sell(today_data)
            elif today_data['open'] > MA_line_5 and today_data['close'] < MA_line_5:
                self.sell(today_data)
            
            if i % 300 == 0:
                Dtemp = self.stock[self.code] * today_data['close'] + self.deposit
                Rtemp = Dtemp - self.capital
                print('[Middle Result]  Deposit : {}, Revenue : {} '.format(Dtemp, Rtemp))
                print()

        self.sell(today_data) # 안 팔아버렸을 수 있음

        revenue = self.deposit - self.capital
        earning_rate = ((self.deposit/self.capital)-1)*100
        
        print('[Final Result]  Deposit : {}, Stock : {}'.format(self.deposit, self.stock[self.code]))
        print('Revenue : {}, Earning rate : {}'.format(revenue, earning_rate))
            

        
        

        
         






if __name__ == "__main__":
    m = ModelBasic(deposit=1*BAEK, code='005930', type='day')
    m.run()