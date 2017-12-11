import sqlite3

DATABASE = 'stock.db'


class Singleton(type):
    _instances = {}
    def __init__(cls, *args, **kwargs):
        cls.conn = sqlite3.connect(DATABASE, check_same_thread=False)

    def __del__(cls):
        cls.conn.close()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class TickerReader(metaclass=Singleton):
    def get_tickers(self, date, limit=10):
        '''
        Get stock tickers with company name
        :param date: YYYYMDD formatted string such as '20171201'
        :param limit: limit value (integer) to be displayed. If not specified, limit is set to 10 
        :return: 
        '''
        print(limit)
        query = 'SELECT ticker, name FROM {} LIMIT {}'.format('TICKER' + date, str(limit))
        curs = self.conn.cursor()
        curs.execute(query)
        return {x[0]: x[1] for x in curs.fetchall()}


class DailyReader(metaclass=Singleton):
    def __init__(self):
        self.ticker = ""
        self.limit = 0
        self.response = []

    def __get_prices__(self, ticker, limit=10):
        '''      
        Get stock price information sorted by date
        :param ticker: stock ticker (string) 
        :param limit: limit value (integer) to be displayed. If not specified, limit is set to 10
        :return: tuple list (date, open price, high price, low price, close price)
                 [(20131118, 5140, 5140, 4965, 5120), (20131115, 5200, 5200, 5100, 5170), ...]
        '''
        if self.ticker != ticker or self.limit != limit:
            self.ticker = ticker
            self.limit = limit
            query = 'SELECT date, open, high, low, close FROM {} ORDER BY date DESC LIMIT {}'.\
                format('S' + ticker, str(limit))
            curs = self.conn.cursor()
            curs.execute(query)
            self.response = curs.fetchall()
        return self.response

    # return tuple list (date/open)
    def get_open(self, ticker, limit=10):
        return {x[0]: x[1] for x in self.__get_prices__(ticker, limit)}

    # return tuple list (date/high)
    def get_high(self, ticker, limit=10):
        return {x[0]: x[2] for x in self.__get_prices__(ticker, limit)}

    # return tuple list (date/low)
    def get_low(self, ticker, limit=10):
        return {x[0]: x[3] for x in self.__get_prices__(ticker, limit)}

    # return tuple list (date/close)
    def get_close(self, ticker, limit=10):
        return {x[0]: x[4] for x in self.__get_prices__(ticker, limit)}

if __name__ == "__main__" :
    res = DailyReader().get_open('000020')
    print(res)
    res = TickerReader().get_tickers('20130401')
    print(id(res))
