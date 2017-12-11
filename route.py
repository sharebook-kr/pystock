from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from dbReader import DailyReader, TickerReader

app = Flask(__name__)
api = Api(app)


class Parser(Resource):
    @staticmethod
    def get_limit():
        parser = reqparse.RequestParser()
        parser.add_argument('limit', type=int)
        limit = parser.parse_args()['limit']
        if limit is None:
            limit = 10
        return limit


class DailyPrice(Parser):
    def get(self, ticker):
        limit = self.get_limit()
        return jsonify(open=DailyReader().get_open(ticker, limit), high=DailyReader().get_high(ticker, limit),
                       low=DailyReader().get_low(ticker, limit), close=DailyReader().get_close(ticker, limit))


class Ticker(Parser):
    def get(self, date):
        limit = self.get_limit()
        print (limit)
        return jsonify(TickerReader().get_tickers(date, limit))


api.add_resource(DailyPrice, '/daily/<string:ticker>')
api.add_resource(Ticker, '/ticker/<string:date>')


if __name__ == '__main__':
    app.run(debug=True)


